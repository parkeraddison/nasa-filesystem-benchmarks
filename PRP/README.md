Nautilus
========

Nautilus uses a Kubernetes cluster so to run a benchmark the process is:
1. Create a volume with the desired filesystem (e.g. Ceph block, POSIX, S3, etc)
2. Create a deployment with an image that has all benchmark software installed and mount it to the desired volume
3. Execute the command to run a benchmark directly on a pod

You will need to be a member of a namespace to do anything. See https://nautilus.optiputer.net

## Volumes

A simple Rook Ceph Block filesystem is defined in `volumes/block.yml`.

To deploy it on Nautilus, run
```
kubectl create -f volumes/block.yml
```

## Deployment

A simple deployment mounted to the ceph block filesystem is defined in `minimal-deploy.yml`.

The image used should be capable of running the desired benchmarks, such as [IOR][ior] or [FIO][fio].

To deploy, run
```
kubectl create -f minimal-deploy.yml
```

## Images

Various images are defined in `Dockerfile.*` and can be built with
```
docker build -t <repo/image_name>:<tag> -f Dockerfile.<name>
```

The current list of images:
- `io500` -- Dependencies to run IOR and IO500 tests
- `fio` -- Dependencies to run FIO tests; built on top of `io500`


<!-- Links -->
[ior]: https://github.com/hpc/ior
[fio]: https://fio.readthedocs.io/en/latest/fio_doc.html#job-file-format
[io500]: https://www.vi4io.org/io500/
