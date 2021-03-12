import shlex
import subprocess
import time
from kopf.testing import KopfRunner

def test_operator():
    with KopfRunner(['run', '--verbose', 'handlers.py']) as runner:
        # do something while the operator is running.

        # subprocess.run("kubectl apply -f examples/obj.yaml",
        #     shell=True, check=True)
        time.sleep(1)

    assert runner.exit_code == 0
    assert runner.exception is None
    # assert 'And here we are!' in runner.stdout
    # assert 'Deleted, really deleted' in runner.stdout


test_operator()
