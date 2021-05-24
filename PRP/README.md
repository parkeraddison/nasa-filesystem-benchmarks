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

The image used should be capable of running the desired benchmarks, such as [IOR] or [FIO].

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
- `kube-openmpi-ior` -- The image used [kube-openmpi] with IOR installed

## MPI jobs

To support running multi-node MPI jobs on the Nautilus cluster, we're using [everpeace/kube-openmpi][kube-openmpi].

### Setup

1. Install [Helm]
2. Clone kube-openmpi and in the directory run `./gen-ssh-key.sh`
3. Edit `values.yaml` with your desired image and resource requests
4. Add the rolebinding
    ```sh
    KUBE_NAMESPACE=my_namespace
    kubectl create -n $KUBE_NAMESPACE -f https://gitlab.com/ucsd-prp/prp_k8s_config/-/raw/master/mpi/rolebindings.yaml
    ```
5. Generate the kube resource yamls and deploy them on the cluster
    ```sh
    # While working directory is PRP/
    make openmpi
    # Or, run the command yourself
    helm template nautilus chart -n $KUBE_NAMESPACE -f values.yaml -f ssh-key.yaml | kubectl -n $KUBE_NAMESPACE create -f -
    ```

### Running

Once all pods are running, you can use `kubectl exec` to run `mpiexec` from the master node.
```sh
# Using the alias defined in the dockerfile
kubectl exec -it nautilus-master -- omexec -npernode 1 -np 4 ior
# or, run the command yourself
kubectl exec -it nautilus-master -- mpiexec --allow-run-as-root --hostfile /kube-openmpi/generated/hostfile --display-map -n 4 -npernode 1 ior
```

## References
- [IOR]
- [FIO]
- [IO500]
- [kube-openmpi]
- [mpiexec]
- [Helm]

[ior]: https://github.com/hpc/ior
[fio]: https://fio.readthedocs.io/en/latest/fio_doc.html#job-file-format
[io500]: https://www.vi4io.org/io500/
[kube-openmpi]: https://github.com/everpeace/kube-openmpi
[mpiexec]: https://linux.die.net/man/1/mpiexec
[helm]: https://helm.sh/docs/intro/quickstart/
