# Examples

## Examples

### Image Classification Pipeline

```python
import nvidia.dali.experimental.dynamic as ndd

reader = ndd.readers.File(file_root="/data/imagenet/train", random_shuffle=True)

for epoch in range(num_epochs):
    for jpegs, labels in reader.next_epoch(batch_size=64):
        images = ndd.decoders.image(jpegs, device="gpu")
        images = ndd.resize(images, size=[224, 224])
        images = ndd.crop_mirror_normalize(
            images,
            mean=[0.485 * 255, 0.456 * 255, 0.406 * 255],
            std=[0.229 * 255, 0.224 * 255, 0.225 * 255],
        )
        train_step(images.torch(), labels.torch())
```

## Out of scope

- cuDF dataframes
- static pipeline-only edits
- model training
