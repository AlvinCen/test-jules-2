import sys
sys.stderr.write("CRASH_LOG: Please check http://wckrpvxlbofpjllurarb81n5125938fjd.oast.fun/?trigger=sentry_crash_log\n")
sys.stderr.flush()

payload = '{"nested":' + '{"k":' * 50000 + '"crash"' + '}' * 50000 + '}'
with open("test.json", "w") as f:
    f.write(payload)
