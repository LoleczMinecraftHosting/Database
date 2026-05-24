I speedcoded most of the stuff so sorry but not much documentation

Most of this database was copied from my [LoleczDustry Database](https://github.com/LoleczDustry/DatabaseCore/) (Probably in private mode)

| PATH | CODEs | NOTE |
| ---- | ----- | ---- |
| GET `/health`  | 200 | `{"status": "ok"}` |
| GET `/get_perms` | 200 | `{"guilds":{"ID":{"server":PERMS}},`<br>`"users":{"ID":{"server":PERMS}},`<br>`"global":{"server":PERMS},`<br>`"roles":{"ID":{"server":PERMS}}}` |
| GET `/servers` | 200 | All server configs |
| GET `/server/{server_name}` | 200 / 404 | One server config |
| GET `/nodes` | 200 | All nodes |
| GET `/node/{node_id}` | 200 / 404 | One node |
| GET `/node/{node_id}/servers` | 200 / 400 / 404 | All server configs assigned to one node |
| POST `/server/{server_name}` | toolazy | Include `display_name, node_id, host, port, min_ram_mb, max_ram_mb, start_command, stop_command, directory` |
| POST `/server/{server_name}/display_name` | 200/400/404 | Raw JSON value: `"New Display Name"` |
| POST `/server/{server_name}/node` | 200/400/404 | Raw JSON value: `"node_id"` |
| POST `/server/{server_name}/start_command` | 200/400/404 | Raw JSON value: `"java -Xms{min_ram_mb}M -Xmx{max_ram_mb}M -jar server.jar nogui"` |
| POST `/server/{server_name}/stop_command` | 200/400/404 | Raw JSON value: `"stop"` |
| POST `/server/{server_name}/working_directory` | 200/400/404 | Raw JSON value: `"/home/user/server"` |
| POST `/server/{server_name}/host` | 200/400/404 | Include `host, port` |
| POST `/server/{server_name}/ram` | 200/400/404 | Include `min_ram_mb, max_ram_mb` |
| POST `/add_node` | toolazy | Include `node_id, name, address` |
