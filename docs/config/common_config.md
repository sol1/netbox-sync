# Common Configuration

Controls the parameters for logging
    

## `log_level`
**Type:** `str`  
**Default:** `INFO`

Logs will always be printed to stdout/stderr.
Logging can be set to following log levels:
  ERROR:      Fatal Errors which stops regular a run
  WARNING:    Warning messages won't stop the syncing process but mostly worth
              to have a look at.
  INFO:       Information about objects that will be create/updated/deleted in NetBox
  DEBUG:      Will log information about retrieved information, changes in internal
              data structure and parsed config
  DEBUG2:     Will also log information about how/why data is parsed or skipped.
  DEBUG3:     Logs all source and NetBox queries/results to stdout. Very useful for
              troubleshooting, but will log any sensitive data contained within a query.
  TRACE:      Same as DEBUG3.

## `log_to_file`
**Type:** `bool`  
**Default:** `False`

Enabling this options will write all logs to a log file defined in 'log_file'

## `log_file`
**Type:** `str`  
**Default:** `log/netbox_sync.log`

Destination of the log file if "log_to_file" is enabled. Log file will be rotated maximum
5 times once the log file reaches size of 10 MB

## `log_lastrun_errors`
**Type:** `bool`  
**Default:** `False`

Enabling this options will write all errors for this run only to a separate file called
'netbox-sync-lastrun-errors.log' in the same directory as netbox-sync.py.

## Example (YAML)

```

common:
  log_level: "INFO"
  log_to_file: false
  log_file: "log/netbox_sync.log"
  log_lastrun_errors: false
```

## Example (INI)

```

[common]
log_level = INFO
log_to_file = false
log_file = log/netbox_sync.log
log_lastrun_errors = false
```

---
