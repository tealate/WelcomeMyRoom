function space_editor:job/unforceload_archive with storage space_editor:document job
execute if data storage space_editor:document job{type:"copy"} run return run function space_editor:copy/finalize
function space_editor:paste/finalize
