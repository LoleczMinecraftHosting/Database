I speedcoded most of the stuff so sorry but not much documentation

Most of this database was copied from my [LoleczDustry Database](https://github.com/LoleczDustry/DatabaseCore/) (Probably in private mode)

| PATH | CODEs | NOTE |
| ---- | ----- | ---- |
| GET /health  | 200 | `{"status": "ok"}` |
| GET /get_perms | 200 | `{"guilds":{"ID":{"server":PERMS}},`<br>`"users":{"ID":{"server":PERMS}},`<br>`"global":{"server":PERMS},`<br>`"roles":{"ID":{"server":PERMS}}}` |
| POST /server/{server_name} | toolazy | Include `display_name, node_id, host, port, min_ram_mb, max_ram_mb, start_command, stop_command, directory` |
| POST /add_node | toolazy | Include `node_id, name, address` |
