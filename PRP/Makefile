# PRP Make Targets
# ================
#
# These are utilities to facilitate running commands.

KUBE_NAMESPACE?=usra-hpc

.PHONY: openmpi
openmpi:
	helm template nautilus kube-openmpi/chart -n ${KUBE_NAMESPACE} -f values.yaml -f kube-openmpi/ssh-key.yaml | kubectl -n ${KUBE_NAMESPACE} apply -f -

.PHONY: openmpi-delete
openmpi-delete:
	helm template nautilus kube-openmpi/chart -n ${KUBE_NAMESPACE} -f values.yaml -f kube-openmpi/ssh-key.yaml | kubectl -n ${KUBE_NAMESPACE} delete -f -



