execute if data storage editor:runtime job{phase:"error"} run return 0
execute if data storage editor:runtime job{phase:"next"} run return run function editor:internal/job/next
execute if data storage editor:runtime job{phase:"wait"} run function editor:internal/job/wait
