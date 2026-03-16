# Logging Framework — Entities, Responsibilities & Interactions

> Bottom-up: from `LogLevel` → `LogManager`

---

## 1. `LogLevel` (Enum)

**Responsibility:** Define severity hierarchy

**Values:** `DEBUG` → `INFO` → `WARN` → `ERROR` → `FATAL`

**Interacts with:** `LogMessage`, `Logger`, `LoggerConfig` — used for level comparison and filtering

---

## 2. `LogMessage` (Data Object)

**Responsibility:** Bundle all log metadata into a single object

**Fields:**

- `level: LogLevel`
- `message: String`
- `timestamp: LocalDateTime`
- `threadName: String`
- `loggerName: String`

**Interacts with:** Created by `Logger` → passed to `AsyncLogProcessor` → `LogAppender` → `LogFormatter`

---

## 3. `LogFormatter` (Interface)

**Responsibility:** Convert `LogMessage` → formatted `String`

**Contract:**

```
format(LogMessage): String
```

**Interacts with:** Held by each `LogAppender`, called inside `append()`

---

## 4. `SimpleTextFormatter` (impl of `LogFormatter`)

**Responsibility:** Produce plain text log line

**Fields:**

- `DATE_TIME_FORMATTER: DateTimeFormatter`

**Interacts with:** Injected into appenders via `setFormatter()`

---

## 5. `LogAppender` (Interface)

**Responsibility:** Define contract for writing logs to a destination

**Contract:**

```
setFormatter(LogFormatter): void
getFormatter(): LogFormatter
append(LogMessage): void
close(): void
```

**Interacts with:** Holds a `LogFormatter`; called by `AsyncLogProcessor`

---

## 6. `ConsoleAppender` / `FileAppender` / `DatabaseAppender` (impl of `LogAppender`)

**Responsibility:** Write formatted log to their respective destination

| Class              | Destination | Extra Field              |
| ------------------ | ----------- | ------------------------ |
| `ConsoleAppender`  | stdout      | —                        |
| `FileAppender`     | file        | `writer: FileWriter`     |
| `DatabaseAppender` | DB          | `connection: Connection` |

**Shared logic:** each calls `formatter.format(logMessage)` → writes output to destination

---

## 7. `LoggerConfig`

**Responsibility:** Hold bootstrap configuration — default `LogLevel` + initial `LogAppender` list

**Fields:**

- `level: LogLevel`
- `appenders: List<LogAppender>`

**Interacts with:** Read by `LogManager` at startup, applied to `rootLogger`

---

## 8. `AsyncLogProcessor`

**Responsibility:** Decouple log call from I/O using a thread pool

**Fields:**

- `executor: ExecutorService`

**Logic:**

```
process(LogMessage, List<LogAppender>)
  → submit task to ExecutorService
  → worker thread calls appender.append(logMessage)
```

**Interacts with:** Receives from `Logger`, fans out to each `LogAppender`

---

## 9. `Logger`

**Responsibility:** Core logging engine — level filtering, message creation, appender fanout

**Fields:**

- `parent: Logger` — for hierarchy
- `appenders: List<LogAppender>`
- `name: String`
- `level: LogLevel`
- `additivity: boolean`

**Key Logic:**

| Method                | What it does                                                                               |
| --------------------- | ------------------------------------------------------------------------------------------ |
| `getEffectiveLevel()` | Walks parent chain until a level is set                                                    |
| `log(level, msg)`     | Filters → builds `LogMessage` → calls `callAppenders()`                                    |
| `callAppenders()`     | Passes to `AsyncLogProcessor`; if `additivity=true`, also propagates to parent's appenders |

**Interacts with:** `AsyncLogProcessor`, `LogAppender`, `LogMessage`, parent `Logger`

---

## 10. `LogManager` (Singleton)

**Responsibility:** Global registry — creates/caches loggers, owns `rootLogger` and `AsyncLogProcessor`

**Fields:**

- `INSTANCE: LogManager`
- `rootLogger: Logger`
- `loggers: Map<String, Logger>`
- `processor: AsyncLogProcessor`

**Key Logic:**

| Method               | What it does                                                |
| -------------------- | ----------------------------------------------------------- |
| `getLogger(name)`    | Returns cached logger or creates new one with parent wired  |
| `createLogger(name)` | Instantiates `Logger`, sets parent, registers in map        |
| `shutdown()`         | Stops `AsyncLogProcessor`, calls `close()` on all appenders |

**Interacts with:** Creates `Logger` instances, reads `LoggerConfig`, manages `AsyncLogProcessor` lifecycle

---

## Data Flow

```
LogManager
  └─→ Logger
        └─→ AsyncLogProcessor
              └─→ LogAppender
                    └─→ LogFormatter
                          └─→ output (console / file / DB)
```

---

## Requirements Mapping

| Requirement            | Design Decision                                                                                                      |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Multiple log levels    | `LogLevel` enum + level check in `Logger.log()`                                                                      |
| Metadata with each log | `LogMessage` bundles level, timestamp, thread, name                                                                  |
| Multiple destinations  | `LogAppender` interface with multiple concrete impls                                                                 |
| Configuration          | `LoggerConfig` applied at bootstrap via `LogManager`                                                                 |
| Thread safety          | `ConcurrentHashMap` in `LogManager`, `ExecutorService` in `AsyncLogProcessor`, synchronized writes in `FileAppender` |
| Extensibility          | New destination = new `LogAppender` impl; new formatter = new `LogFormatter` impl                                    |
