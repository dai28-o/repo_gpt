from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang=\"ja\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <title>ToDoリスト</title>
        <style>
            :root {
                color-scheme: light dark;
                --bg-color: #f3f4f6;
                --card-color: #ffffffcc;
                --text-color: #111827;
                --accent: #2563eb;
                --accent-dark: #1d4ed8;
                --danger: #ef4444;
                --danger-dark: #dc2626;
            }

            body {
                font-family: \"Segoe UI\", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
                margin: 0;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background: var(--bg-color);
                color: var(--text-color);
            }

            .app-shell {
                width: min(480px, 92vw);
                background: var(--card-color);
                backdrop-filter: blur(12px);
                padding: 24px 20px 32px;
                border-radius: 24px;
                box-shadow: 0 20px 35px rgba(15, 23, 42, 0.15);
            }

            h1 {
                margin-top: 0;
                text-align: center;
                font-size: clamp(1.6rem, 6vw, 2.4rem);
                letter-spacing: 0.03em;
            }

            .input-row {
                display: flex;
                gap: 12px;
                margin-bottom: 24px;
            }

            input[type=\"text\"] {
                flex: 1;
                padding: 16px 18px;
                font-size: 1.1rem;
                border: 2px solid rgba(99, 102, 241, 0.35);
                border-radius: 16px;
                outline: none;
                transition: border-color 0.2s ease, box-shadow 0.2s ease;
            }

            input[type=\"text\"]:focus {
                border-color: var(--accent);
                box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.15);
            }

            button {
                border: none;
                border-radius: 16px;
                font-size: 1.1rem;
                padding: 16px 24px;
                cursor: pointer;
                font-weight: 600;
                transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.2s ease;
            }

            button:active {
                transform: scale(0.97);
            }

            .add-btn {
                background: var(--accent);
                color: white;
                min-width: 120px;
                box-shadow: 0 10px 20px rgba(37, 99, 235, 0.25);
            }

            .add-btn:hover {
                background: var(--accent-dark);
            }

            ul {
                list-style: none;
                padding: 0;
                margin: 0;
                display: flex;
                flex-direction: column;
                gap: 12px;
            }

            li {
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: rgba(255, 255, 255, 0.9);
                border-radius: 18px;
                padding: 16px 18px;
                box-shadow: 0 10px 18px rgba(15, 23, 42, 0.08);
                font-size: 1.05rem;
            }

            .task-text {
                flex: 1;
                margin-right: 12px;
                word-break: break-word;
            }

            .delete-btn {
                background: var(--danger);
                color: white;
                padding: 14px 20px;
                box-shadow: 0 8px 16px rgba(239, 68, 68, 0.25);
            }

            .delete-btn:hover {
                background: var(--danger-dark);
            }

            .empty-message {
                text-align: center;
                color: #6b7280;
                font-size: 1rem;
                margin-top: 12px;
            }

            @media (prefers-color-scheme: dark) {
                :root {
                    --bg-color: #0f172a;
                    --card-color: rgba(15, 23, 42, 0.85);
                    --text-color: #f8fafc;
                }

                li {
                    background: rgba(30, 41, 59, 0.9);
                }
            }
        </style>
    </head>
    <body>
        <main class=\"app-shell\">
            <h1>My ToDoリスト</h1>
            <form class=\"input-row\" id=\"task-form\">
                <input id=\"task-input\" type=\"text\" placeholder=\"タスクを入力\" aria-label=\"タスク名\" required>
                <button type=\"submit\" class=\"add-btn\">追加</button>
            </form>
            <ul id=\"task-list\"></ul>
            <p id=\"empty-message\" class=\"empty-message\">まだタスクがありません。追加してみましょう！</p>
        </main>

        <script>
            const form = document.getElementById('task-form');
            const input = document.getElementById('task-input');
            const list = document.getElementById('task-list');
            const emptyMessage = document.getElementById('empty-message');

            const updateEmptyState = () => {
                const hasTasks = list.children.length > 0;
                emptyMessage.style.display = hasTasks ? 'none' : 'block';
            };

            const createTaskItem = (text) => {
                const li = document.createElement('li');

                const span = document.createElement('span');
                span.textContent = text;
                span.className = 'task-text';
                li.appendChild(span);

                const deleteButton = document.createElement('button');
                deleteButton.textContent = '削除';
                deleteButton.className = 'delete-btn';
                deleteButton.type = 'button';
                deleteButton.addEventListener('click', () => {
                    li.remove();
                    updateEmptyState();
                });

                li.appendChild(deleteButton);
                return li;
            };

            form.addEventListener('submit', (event) => {
                event.preventDefault();
                const text = input.value.trim();
                if (!text) {
                    input.focus();
                    return;
                }

                const item = createTaskItem(text);
                list.appendChild(item);
                input.value = '';
                input.focus();
                updateEmptyState();
            });

            updateEmptyState();
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
