### Pellet metrics

| Name               | Key                  | Unbinned                                                     | Binned                                                       | Notes                                                        |
| ------------------ | -------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Pellets            | `pellets`            | Running cumulative count of pellets (essentially the `"Pellet_Count"` column) | Count of pellets retrieved within each temporal bin          | Behavior of `cumulative pellets` when data are not binned, and behavior of `binary_pellets` otherwise. |
| Binary Pellets     | `binary_pellets`     | Binary series indicating when pellets are returned.          | Count of pellets retrieved within each temporal bin          |                                                              |
| Cumulative Pellets | `cumulative_pellets` | Running cumulative count of pellets (essentially the `"Pellet_Count"` column) | Maximum value of the running cumulative pellet count within each bin | This can be used when plotting to explicitly create average, cumulative pellet retrieval (as opposed to non-cumulative). |

### Poke metrics - general

These are metrics that measure pokes, without regard for their side (left/right) or correctness.

| Name             | Key                | Notes                                                        |
| :--------------- | :----------------- | :----------------------------------------------------------- |
| Pokes            | `pokes`            | Behavior of `cumulative_pokes` when data are not binned, and behavior of `binary_pokes` otherwise. |
| Binary Pokes     | `binary_pokes`     |                                                              |
| Cumulative Pokes | `cumulative_pokes` |                                                              |