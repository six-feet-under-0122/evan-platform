import multiprocessing

# ── 绑定地址 ──────────────────────────────────────────
bind = "127.0.0.1:8000"
# 只监听本机，不对外暴露。外部请求由 Caddy 反向代理进来。
# 不要写 0.0.0.0，那样会直接暴露到公网，绕过 Caddy 的 HTTPS。

# ── Worker 进程数 ─────────────────────────────────────
workers = multiprocessing.cpu_count() * 2 + 1
# 经典公式：CPU 核心数 × 2 + 1
# 比如 2 核 VPS → 5 个 worker
# 每个 worker 是独立进程，互不干扰，一个挂了其他继续跑

# ── Worker 类型 ───────────────────────────────────────
worker_class = "gthread"
# 默认的 "sync" worker 每个进程同时只处理一个请求
# "gthread" 是多线程 worker，每个进程可以同时处
# SSE 长连接会占住一个线程，用 gthread 才不会把所有 worker 都堵死

threads = 4
# 每个 worker 开 4 个线程，总并发 = workers × t

# ── 超时 ──────────────────────────────────────────────
timeout = 120
# worker 处理一个请求超过 120 秒就被 kill 重启
# 注意：SSE 是长连接，但 SSE 的每个 chunk 都在动，不会触发这个超时
# 这个超时针对的是"worker 完全没有响应"的情况

keepalive = 5
# HTTP Keep-Alive：连接复用等待时间（秒）
# 客户端发完请求后，连接保持 5 秒，期间可以复用发下一个请求

# ── 日志 ──────────────────────────────────────────────
accesslog = "-"
# "-" 表示输出到 stdout，方便 systemd/Docker 收集日志

errorlog = "-"
# 错误日志同样输出到 stdout

loglevel = "info"
# 日志级别：debug / info / warning / error / critical

# ── 进程管理 ──────────────────────────────────────────
preload_app = True
# 主进程先加载 Flask app，fork 出 worker 时直接复制内存
# 好处：省内存（共享代码段），启动更快
# 注意：数据库连接要在 worker 里初始化，不能在 preload 阶段建立

pidfile = "/tmp/gunicorn.pid"
# 把主进程的 PID 写到这个文件，方便脚本做 reload/stop
