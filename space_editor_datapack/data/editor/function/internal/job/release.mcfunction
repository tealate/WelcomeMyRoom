execute unless data storage editor:runtime job.tickets[0] run return 0
function editor:internal/job/unticket with storage editor:runtime job.tickets[0]
data remove storage editor:runtime job.tickets[0]
function editor:internal/job/release
