"""Isolated GPU experiments. Reports distinguish machine metrics from human judgment."""
import gc
import hashlib
import json
import os
import random
import re
import sys
import time
from pathlib import Path

os.environ.setdefault('HF_HUB_DISABLE_TELEMETRY', '1')
os.environ.setdefault('DO_NOT_TRACK', '1')


def rows(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


def stage(output, value, label):
    temporary = output / 'progress.tmp'
    temporary.write_text(json.dumps({'progress': value, 'stage': label}), encoding='utf-8')
    temporary.replace(output / 'progress.json')


def ece(pairs):
    result = 0
    for index in range(10):
        bucket = [(confidence, correct) for confidence, correct in pairs if index / 10 <= confidence <= (index + 1) / 10
                  and (index == 9 or confidence < (index + 1) / 10)]
        if bucket:
            result += abs(sum(c for c, _ in bucket) - sum(k for _, k in bucket)) / max(1, len(pairs))
    return result


def evaluate_laya(model_path, test):
    import laya
    model = laya.load(model_path, device='cuda')
    metrics = {'strategy': [], 'relevance': []}
    started = time.perf_counter()
    for row in test:
        prediction = model.predict(row['state'], row['questions'])['answers']
        for question in metrics:
            answer = prediction[question]
            values = answer['probabilities']
            selected = max(values, key=values.get)
            expected = str(row.get('expected', row.get('gold'))[question])
            metrics[question].append((float(values[selected]), selected == expected))
    result = {name: {'accuracy': sum(c for _, c in pairs) / max(1, len(pairs)), 'ece': ece(pairs), 'count': len(pairs)}
              for name, pairs in metrics.items()}
    result['latency_ms'] = (time.perf_counter() - started) * 1000 / max(1, len(test))
    del model
    gc.collect()
    import torch
    torch.cuda.empty_cache()
    return result


def load_llm(model_name, adapter=None):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=False)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map='auto', trust_remote_code=False,
        quantization_config=BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4',
                                              bnb_4bit_compute_dtype=torch.bfloat16))
    if adapter:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, adapter)
    return model, tokenizer


def f1(prediction, expected):
    from collections import Counter
    a = Counter(re.findall(r'\w+', prediction.lower()))
    b = Counter(re.findall(r'\w+', expected.lower()))
    overlap = sum((a & b).values())
    return 2 * overlap / max(1, sum(a.values()) + sum(b.values()))


def evaluate_llm(model_name, test, adapter=None):
    import torch
    model, tokenizer = load_llm(model_name, adapter)
    model.eval()
    values, citations, abstention = [], [], []
    started = time.perf_counter()
    for row in test:
        prompt = tokenizer.apply_chat_template(row['messages'][:-1], tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(prompt, return_tensors='pt').to(model.device)
        with torch.inference_mode():
            answer = model.generate(**inputs, max_new_tokens=256, do_sample=False)
        text = tokenizer.decode(answer[0, inputs.input_ids.shape[1]:], skip_special_tokens=True)
        values.append(f1(text, row['answer']))
        negative = row['context'] == 'No evidence was retrieved.'
        cites = re.findall(r'\[(\d+)\]', text)
        citations.append((not cites) if negative else bool(cites) and all(n == '1' for n in cites))
        if negative:
            abstention.append(bool(re.search(r'insuficiente|não há|não encontrei|insufficient|cannot|no evidence', text, re.I)))
    result = {'reference_token_f1': sum(values) / max(1, len(values)),
              'citation_format_validity': sum(citations) / max(1, len(citations)),
              'negative_abstention': sum(abstention) / max(1, len(abstention)), 'count': len(test),
              'latency_ms': (time.perf_counter() - started) * 1000 / max(1, len(test)),
              'scope': 'Reference overlap and citation format, not verified entailment or factual correctness'}
    del model
    gc.collect()
    torch.cuda.empty_cache()
    return result


def main(config):
    import torch
    if not torch.cuda.is_available():
        raise ValueError('CUDA is required for domain training; install the locked CUDA wheel')
    torch.manual_seed(config['seed'])
    random.seed(config['seed'])
    output = Path(config['output'])
    stage(output, .05, 'preflight')
    folder = Path(config['dataset']) / config['flow']
    validation = rows(folder / 'validation.jsonl')
    report = {'flow': config['flow'], 'seed': config['seed'], 'gpu': torch.cuda.get_device_name(),
              'torch': torch.__version__, 'promoted': False, 'human_reviewed': False,
              'dataset_hashes': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob('*.jsonl')}}
    if config['flow'] == 'llm':
        from huggingface_hub import snapshot_download
        original_model = config['llm_model']
        base = (str(Path(original_model).resolve()) if Path(original_model).is_dir() else
                snapshot_download(original_model, allow_patterns=['*.json', '*.safetensors', '*.txt', '*.model']))
        config['llm_model'] = base
        report.update(base_model=original_model, base_revision=Path(base).name)
    if config['action'] == 'evaluate':
        test = rows(output / 'test.jsonl')
        if config['flow'] == 'laya':
            report['baseline'] = evaluate_laya(config['laya_model'], test)
            if config.get('checkpoint'):
                report['candidate'] = evaluate_laya(config['checkpoint'], test)
        else:
            report['baseline'] = evaluate_llm(config['llm_model'], test)
            if config.get('checkpoint'):
                report['candidate'] = evaluate_llm(config['llm_model'], test, config['checkpoint'])
    elif config['flow'] == 'laya':
        from huggingface_hub import snapshot_download
        from laya import load
        from laya.train import TrainConfig, dry_run, finetune
        # Store exact base checkpoint identity before train starts.
        base = snapshot_download(config['laya_model'])
        report['base_revision'] = Path(base).name
        report['baseline'] = evaluate_laya(base, validation)
        (output / 'baseline.json').write_text(json.dumps(report, indent=2, default=str), encoding='utf-8')
        stage(output, .15, 'baseline-evaluated')
        # Validate tensor construction and a real forward pass before the training loop.
        preflight = load(base, device='cuda')
        original_rows = rows(folder / 'train.jsonl')
        first = original_rows[0]
        preflight.predict(first['state'], first['questions'])
        del preflight
        gc.collect()
        torch.cuda.empty_cache()
        converted = output / 'inputs'
        converted.mkdir()
        for part in ['train', 'validation']:
            adapted = []
            for row in rows(folder / f'{part}.jsonl'):
                # SDK gold is a probability distribution; scalar labels use expected.
                if isinstance(row.get('gold'), dict) and all(not isinstance(v, dict) for v in row['gold'].values()):
                    row = {**row, 'expected': row['gold']}
                    row.pop('gold')
                adapted.append(row)
            (converted / f'{part}.jsonl').write_text(''.join(json.dumps(row, ensure_ascii=False)+'\n' for row in adapted), encoding='utf-8')
        training = TrainConfig(epochs=config['epochs'], micro_batch=1, grad_accum=8, loss='rlcd',
            max_len=1024, seed=config['seed'], amp=True, gradient_checkpointing=True,
            shuffle_options=('choice',), calib_seed=config['seed'], log_every=10,
            eval_data=str(converted / 'validation.jsonl'))
        report['preprocessing'] = dry_run(str(converted / 'train.jsonl'), base, training)
        summary = finetune(str(converted / 'train.jsonl'), base, str(output / 'checkpoint'), training, device='cuda')
        stage(output, .85, 'training-completed')
        report['training'] = summary
        report['candidate'] = evaluate_laya(str(output / 'checkpoint'), validation)
        report['selection_set'] = 'validation; human test remains untouched'
    else:
        from datasets import Dataset
        from peft import LoraConfig
        from transformers import TrainerCallback
        from trl import SFTConfig

        from app.portable_sft import trainer_class
        report['baseline'] = evaluate_llm(config['llm_model'], validation)
        (output / 'baseline.json').write_text(json.dumps(report, indent=2, default=str), encoding='utf-8')
        stage(output, .15, 'baseline-evaluated')
        model, tokenizer = load_llm(config['llm_model'])
        report['base_revision'] = getattr(model.config, '_commit_hash', None) or report['base_revision']
        train_rows = rows(folder / 'train.jsonl')
        train_data = Dataset.from_list([{'prompt': r['messages'][:-1], 'completion': [r['messages'][-1]]}
                                        for r in train_rows])
        args = SFTConfig(output_dir=str(output / 'trainer'), num_train_epochs=config['epochs'],
            per_device_train_batch_size=1, gradient_accumulation_steps=8, max_length=1024,
            learning_rate=2e-4, bf16=True, gradient_checkpointing=True, logging_steps=10,
            save_strategy='epoch', report_to='none', seed=config['seed'], completion_only_loss=True)
        class Progress(TrainerCallback):
            def on_step_end(self, args, state, control, **kwargs):
                stage(output, .2 + .6 * state.global_step / max(1, state.max_steps), 'training')

        report['loss_backend'] = 'Transformers causal cross entropy; completion-masked labels; no Triton'
        trainer = trainer_class()(model=model, args=args, train_dataset=train_data, processing_class=tokenizer,
            callbacks=[Progress()],
            peft_config=LoraConfig(r=16, lora_alpha=32, lora_dropout=.05, target_modules='all-linear',
                                   task_type='CAUSAL_LM'))
        # A failed step aborts without promoting or replacing any serving checkpoint.
        trainer.train()
        trainer.save_model(str(output / 'checkpoint'))
        tokenizer.save_pretrained(output / 'checkpoint')
        stage(output, .85, 'checkpoint-saved')
        del trainer, model
        gc.collect()
        torch.cuda.empty_cache()
        report['candidate'] = evaluate_llm(config['llm_model'], validation, str(output / 'checkpoint'))
        report['selection_set'] = 'validation; human test remains untouched'
    (output / 'result.json').write_text(json.dumps(report, indent=2, default=str), encoding='utf-8')
    print(json.dumps({'status': 'completed', 'report': str(output / 'result.json')}))


if __name__ == '__main__':
    config = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    try:
        main(config)
    except Exception as exc:
        message = str(exc)
        for key, value in os.environ.items():
            if len(value) >= 6 and any(word in key.upper() for word in ['TOKEN', 'PASSWORD', 'SECRET', 'API_KEY']):
                message = message.replace(value, '[redacted]')
        message = re.sub(r'https?://\S+', '[provider URL redacted]', message)
        failure = {'status': 'failed', 'error_type': type(exc).__name__, 'message': message[:500], 'promoted': False}
        (Path(config['output']) / 'failure.json').write_text(json.dumps(failure), encoding='utf-8')
        raise
