"""Dimension union queries with coherent snapshots and bounded, optional area indexes.

Only search data is cached. The document remains authoritative; equality checking
once per tick also catches console edits, undo, demo APIs and future edit paths.
"""
S = 'storage space_editor:search'
P = 'storage space_editor:projection'
R = 'storage space_editor:runtime'
D = 'storage space_editor:document'


def generate(g):
    fn = lambda n, lines: g.fn('search/' + n, lines)
    g.append(g.F / 'load.mcfunction', ['data remove ' + S + ' snapshot'])
    g.insert_before(g.F / 'tick.mcfunction', 'function space_editor:projection/maintenance', ['function space_editor:search/tick'])
    fn('tick', [
        'scoreboard players add #revision pr.v 0',
        'scoreboard players set #changed pr.v 0',
        f'execute if data {D} regions store success score #changed pr.v run data modify {S} snapshot set from {D} regions',
        f'execute unless data {D} regions store success score #changed pr.v run data modify {S} snapshot set value []',
        'execute if score #changed pr.v matches 1 run function space_editor:search/invalidate',
        'scoreboard players set #search_budget pr.v 64',
        *[f'execute if data {S} buildAreas[0] run function space_editor:search/build_step'] * 8,
    ])
    fn('invalidate', [
        'scoreboard players add #revision pr.v 1',
        f'data modify {S} index set value []', f'data remove {S} building',
        f'data modify {S} existence set value []', f'data modify {S} areas set value []',
        f'data modify {S} existence append from {S} snapshot[{{kind:"proxy_existence"}}]',
        f'data modify {S} areas append from {S} snapshot[{{kind:"search_area"}}]',
        f'data modify {S} buildAreas set from {S} areas',
    ])
    fn('build_step', [
        f'execute unless data {S} building run function space_editor:search/build_begin',
        f'execute if data {S} buildCandidates[0] run function space_editor:search/build_candidate',
        f'execute unless data {S} buildCandidates[0] run function space_editor:search/build_finish',
    ])
    fn('build_begin', [
        f'data modify {S} building set from {S} buildAreas[0]',
        f'data modify {S} building.candidates set value []',
        f'data modify {S} buildCandidates set value []',
        f'function space_editor:search/build_dimension with {S} building',
        *[f'execute store result score #area_{a}{b} pr.v run data get {S} building.{a}{b}m' for a in 'xyz' for b in (1, 2)],
    ])
    fn('build_dimension', [f'$data modify {S} buildCandidates append from {S} existence[{{dimension:"$(dimension)"}}]'])
    fn('build_candidate', [
        f'data modify {S} candidate set from {S} buildCandidates[0]', f'data remove {S} buildCandidates[0]',
        'function space_editor:search/overlap',
    ])
    fn('overlap', [line for a in 'xyz' for line in (
        f'execute store result score #bound pr.v run data get {S} candidate.{a}1m',
        f'execute if score #bound pr.v >= #area_{a}2 pr.v run return 0',
        f'execute store result score #bound pr.v run data get {S} candidate.{a}2m',
        f'execute if score #bound pr.v <= #area_{a}1 pr.v run return 0',
    )] + [f'data modify {S} building.candidates append from {S} candidate'])
    fn('build_finish', [f'data modify {S} building.complete set value 1b', f'data modify {S} index append from {S} building', f'data remove {S} buildAreas[0]', f'data remove {S} building'])
    # Query uses route.dimension and #sp{x,y,z} (half milliblocks). A complete
    # index for ANY containing area covers every possible hit at that point.
    fn('query', [
        'scoreboard players set #exists pr.v 0', 'scoreboard players set #pending pr.v 0',
        'scoreboard players set #cache_revision pr.v -1',
        f'execute store result score #cache_revision pr.v run data get {P} route.searchRevision',
        'execute unless score #cache_revision pr.v = #revision pr.v run function space_editor:search/reset_route',
        f'execute if data {P} route.existenceCache run function space_editor:search/cache',
        'execute if score #exists pr.v matches 1 run return 1',
        f'execute unless data {P} route.searchQueue run function space_editor:search/begin with {P} route',
        'function space_editor:search/scan',
        f'execute unless score #exists pr.v matches 1 if data {P} route.searchQueue[0] run scoreboard players set #pending pr.v 1',
        # Completed negatives are not retained on a live route (it is deleted).
    ])
    fn('reset_route', [f'data remove {P} route.existenceCache', f'data remove {P} route.searchQueue', f'data remove {P} route.searchPoint', f'data remove {P} route.searchCert',
        f'execute store result {P} route.searchRevision int 1 run scoreboard players get #revision pr.v'])
    fn('cache', [f'function space_editor:search/fast_contains with {P} route.existenceCache'])
    fn('fast_contains', ['$execute if score #spx se.v matches $(xlo)..$(xhi) if score #spy se.v matches $(ylo)..$(yhi) if score #spz se.v matches $(zlo)..$(zhi) run scoreboard players set #exists pr.v 1'])
    fn('cache_bounds', [line for a in 'xyz' for line in (
        f'execute store result {P} route.existenceCache.{a}lo int 1 run data get {R} spatialRegion.{a}1m 2',
        f'execute store result score #cache_hi pr.v run data get {R} spatialRegion.{a}2m 2',
        'scoreboard players remove #cache_hi pr.v 1',
        f'execute store result {P} route.existenceCache.{a}hi int 1 run scoreboard players get #cache_hi pr.v',
    )])
    fn('check', [f'$execute in $(dimension) run function space_editor:mapping/contains with {R} spatialRegion'])
    fn('begin', [
        f'data modify {S} queryAreas set value []', f'$data modify {S} queryAreas append from {S} index[{{dimension:"$(dimension)",complete:1b}}]',
        f'data remove {S} chosen', 'function space_editor:search/choose_area',
        f'data modify {P} route.searchQueue set value []',
        f'execute if data {S} chosen run data modify {P} route.searchQueue set from {S} chosen.candidates',
        f'$execute unless data {S} chosen run data modify {P} route.searchQueue append from {S} existence[{{dimension:"$(dimension)"}}]',
        f'data modify {P} route.searchCert set value {{xlo:-2147483648,xhi:2147483647,ylo:-2147483648,yhi:2147483647,zlo:-2147483648,zhi:2147483647}}',
        f'execute if data {S} chosen run function space_editor:search/cert_area',
    ])
    fn('choose_area', [
        f'execute unless data {S} queryAreas[0] run return 0',
        'execute if score #search_budget pr.v matches ..0 run return 0',
        'scoreboard players remove #search_budget pr.v 1',
        f'data modify {R} spatialRegion set from {S} queryAreas[0]',
        f'function space_editor:search/check with {P} route',
        f'execute if score #inside se.v matches 1 run return run data modify {S} chosen set from {S} queryAreas[0]',
        f'data remove {S} queryAreas[0]', 'function space_editor:search/choose_area',
    ])
    fn('scan', [
        f'execute unless data {P} route.searchQueue[0] run return 0',
        'execute if score #search_budget pr.v matches ..0 run return 0',
        'scoreboard players remove #search_budget pr.v 1',
        f'data modify {R} spatialRegion set from {P} route.searchQueue[0]',
        f'function space_editor:search/check with {P} route',
        'execute if score #inside se.v matches 1 run return run function space_editor:search/hit',
        'function space_editor:search/exclude', f'data remove {P} route.searchQueue[0]', 'function space_editor:search/scan',
    ])
    fn('hit', [f'data modify {P} route.existenceCache set value {{}}', 'function space_editor:search/cache_bounds',
        f'data remove {P} route.searchQueue', f'data remove {P} route.searchPoint', f'data remove {P} route.searchCert', 'scoreboard players set #exists pr.v 1'])
    # Each rejection intersects an axis-aligned certificate on which it is
    # still a rejection. A moving point can continue a partial scan within this
    # box. Crossing it restarts, so no old negative can delete a valid route.
    fn('cert_check', ['scoreboard players set #cert_ok pr.v 0',
        '$execute if score #spx se.v matches $(xlo)..$(xhi) if score #spy se.v matches $(ylo)..$(yhi) if score #spz se.v matches $(zlo)..$(zhi) run scoreboard players set #cert_ok pr.v 1'])
    fn('cert_area', [line for a in 'xyz' for line in (
        f'execute store result {P} route.searchCert.{a}lo int 1 run data get {S} chosen.{a}1m 2',
        f'execute store result score #bound pr.v run data get {S} chosen.{a}2m 2',
        'scoreboard players remove #bound pr.v 1',
        f'execute store result {P} route.searchCert.{a}hi int 1 run scoreboard players get #bound pr.v',
    )])
    fn('exclude', [line for a in 'xyz' for line in (
        f'execute store result score #bound pr.v run data get {R} spatialRegion.{a}1m 2',
        f'execute if score #sp{a} se.v < #bound pr.v run return run function space_editor:search/exclude_{a}_hi',
        f'execute store result score #bound pr.v run data get {R} spatialRegion.{a}2m 2',
        f'execute if score #sp{a} se.v >= #bound pr.v run return run function space_editor:search/exclude_{a}_lo',
    )])
    for a in 'xyz':
        for side, op in (('lo','>'),('hi','<')):
            fn(f'exclude_{a}_{side}', (['scoreboard players remove #bound pr.v 1'] if side == 'hi' else []) + [
                f'execute store result score #cert_bound pr.v run data get {P} route.searchCert.{a}{side}',
                f'scoreboard players operation #cert_bound pr.v {op} #bound pr.v',
                f'execute store result {P} route.searchCert.{a}{side} int 1 run scoreboard players get #cert_bound pr.v'])
    path = g.F / 'search/query.mcfunction'
    text = path.read_text(encoding='utf-8')
    anchor = f'execute unless data {P} route.searchQueue'
    lines = ['scoreboard players set #cert_ok pr.v 0',
             f'execute if data {P} route.searchCert run function space_editor:search/cert_check with {P} route.searchCert',
             f'execute unless score #cert_ok pr.v matches 1 run data remove {P} route.searchQueue']
    g.write(path, text.replace(anchor, '\n'.join(lines) + '\n' + anchor))
