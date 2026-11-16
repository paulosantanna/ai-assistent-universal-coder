"""TRL data preparation with the public Transformers loss extension point."""


def trainer_class():
    from transformers import Trainer
    from trl import SFTTrainer

    class TorchLossSFTTrainer(SFTTrainer):
        def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
            # TRL1.15's fused LM head calls an unavailable Triton function on Windows.
            # Standard causal CE consumes the same completion-masked labels and PEFT weights.
            return Trainer.compute_loss(self, model, inputs, return_outputs=return_outputs,
                                        num_items_in_batch=num_items_in_batch)

    return TorchLossSFTTrainer
