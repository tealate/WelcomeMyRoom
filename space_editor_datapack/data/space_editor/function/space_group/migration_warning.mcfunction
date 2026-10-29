data modify storage space_editor:runtime sgWarning set value {reason:"invalid_or_conflicting_legacy_pair_unchanged"}
data modify storage space_editor:runtime sgWarning.pairId set from storage space_editor:runtime sgLegacy.id
data modify storage space_editor:runtime spaceLinkWarnings append from storage space_editor:runtime sgWarning
