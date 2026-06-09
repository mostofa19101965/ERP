// Todo List Application with Local Storage

class TodoApp {
    constructor() {
        this.todos = [];
        this.currentFilter = 'all';
        this.editingId = null;
        this.storageKey = 'todoListApp_todos';
        
        this.initializeElements();
        this.loadTodos();
        this.setupEventListeners();
        this.render();
    }

    // Initialize DOM elements
    initializeElements() {
        this.input = document.getElementById('todoInput');
        this.addBtn = document.getElementById('addBtn');
        this.todoList = document.getElementById('todoList');
        this.emptyState = document.getElementById('emptyState');
        
        // Stats
        this.totalTasks = document.getElementById('totalTasks');
        this.completedTasks = document.getElementById('completedTasks');
        this.remainingTasks = document.getElementById('remainingTasks');
        
        // Filter buttons
        this.filterBtns = document.querySelectorAll('.filter-btn');
        
        // Action buttons
        this.clearCompletedBtn = document.getElementById('clearCompleted');
        this.clearAllBtn = document.getElementById('clearAll');
        this.exportBtn = document.getElementById('exportBtn');
        
        // Modal elements
        this.modal = document.getElementById('editModal');
        this.editInput = document.getElementById('editInput');
        this.saveBtn = document.getElementById('saveBtn');
        this.cancelBtn = document.getElementById('cancelBtn');
    }

    // Setup event listeners
    setupEventListeners() {
        // Add task
        this.addBtn.addEventListener('click', () => this.addTodo());
        this.input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addTodo();
        });

        // Filter
        this.filterBtns.forEach(btn => {
            btn.addEventListener('click', (e) => this.filterTodos(e.target.dataset.filter));
        });

        // Action buttons
        this.clearCompletedBtn.addEventListener('click', () => this.clearCompleted());
        this.clearAllBtn.addEventListener('click', () => this.clearAll());
        this.exportBtn.addEventListener('click', () => this.exportTasks());

        // Modal
        this.saveBtn.addEventListener('click', () => this.saveEdit());
        this.cancelBtn.addEventListener('click', () => this.closeModal());
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) this.closeModal();
        });
    }

    // Load todos from local storage
    loadTodos() {
        const stored = localStorage.getItem(this.storageKey);
        if (stored) {
            this.todos = JSON.parse(stored);
        }
    }

    // Save todos to local storage
    saveTodos() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.todos));
    }

    // Add new todo
    addTodo() {
        const text = this.input.value.trim();
        
        if (!text) {
            this.showNotification('Please enter a task!', 'error');
            return;
        }

        if (text.length > 200) {
            this.showNotification('Task is too long (max 200 characters)', 'error');
            return;
        }

        const todo = {
            id: Date.now(),
            text: this.escapeHtml(text),
            completed: false,
            createdAt: new Date().toLocaleString(),
            updatedAt: new Date().toLocaleString()
        };

        this.todos.unshift(todo);
        this.saveTodos();
        this.input.value = '';
        this.render();
        this.showNotification('Task added successfully! ✓', 'success');
    }

    // Toggle todo completion
    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.completed = !todo.completed;
            todo.updatedAt = new Date().toLocaleString();
            this.saveTodos();
            this.render();
        }
    }

    // Edit todo
    editTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            this.editingId = id;
            this.editInput.value = this.unescapeHtml(todo.text);
            this.openModal();
        }
    }

    // Save edit
    saveEdit() {
        const text = this.editInput.value.trim();
        
        if (!text) {
            this.showNotification('Task cannot be empty!', 'error');
            return;
        }

        if (text.length > 200) {
            this.showNotification('Task is too long (max 200 characters)', 'error');
            return;
        }

        const todo = this.todos.find(t => t.id === this.editingId);
        if (todo) {
            todo.text = this.escapeHtml(text);
            todo.updatedAt = new Date().toLocaleString();
            this.saveTodos();
            this.closeModal();
            this.render();
            this.showNotification('Task updated! ✓', 'success');
        }
    }

    // Delete todo
    deleteTodo(id) {
        if (confirm('Are you sure you want to delete this task?')) {
            this.todos = this.todos.filter(t => t.id !== id);
            this.saveTodos();
            this.render();
            this.showNotification('Task deleted! ✓', 'success');
        }
    }

    // Clear completed todos
    clearCompleted() {
        const completedCount = this.todos.filter(t => t.completed).length;
        if (completedCount === 0) {
            this.showNotification('No completed tasks to clear!', 'info');
            return;
        }

        if (confirm(`Delete ${completedCount} completed task(s)?`)) {
            this.todos = this.todos.filter(t => !t.completed);
            this.saveTodos();
            this.render();
            this.showNotification(`Cleared ${completedCount} completed task(s)! ✓`, 'success');
        }
    }

    // Clear all todos
    clearAll() {
        if (this.todos.length === 0) {
            this.showNotification('No tasks to clear!', 'info');
            return;
        }

        if (confirm('Delete all tasks? This cannot be undone!')) {
            this.todos = [];
            this.saveTodos();
            this.render();
            this.showNotification('All tasks cleared! ✓', 'success');
        }
    }

    // Filter todos
    filterTodos(filter) {
        this.currentFilter = filter;
        
        // Update active button
        this.filterBtns.forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.filter === filter) {
                btn.classList.add('active');
            }
        });
        
        this.render();
    }

    // Get filtered todos
    getFilteredTodos() {
        switch (this.currentFilter) {
            case 'active':
                return this.todos.filter(t => !t.completed);
            case 'completed':
                return this.todos.filter(t => t.completed);
            default:
                return this.todos;
        }
    }

    // Export tasks as JSON
    exportTasks() {
        if (this.todos.length === 0) {
            this.showNotification('No tasks to export!', 'info');
            return;
        }

        const dataStr = JSON.stringify(this.todos, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `todo-list-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        
        this.showNotification(`Exported ${this.todos.length} task(s)! ✓`, 'success');
    }

    // Modal functions
    openModal() {
        this.modal.classList.add('active');
        this.editInput.focus();
    }

    closeModal() {
        this.modal.classList.remove('active');
        this.editingId = null;
        this.editInput.value = '';
    }

    // Update statistics
    updateStats() {
        const total = this.todos.length;
        const completed = this.todos.filter(t => t.completed).length;
        const remaining = total - completed;

        this.totalTasks.textContent = total;
        this.completedTasks.textContent = completed;
        this.remainingTasks.textContent = remaining;
    }

    // Render UI
    render() {
        this.updateStats();
        const filteredTodos = this.getFilteredTodos();

        if (filteredTodos.length === 0) {
            this.todoList.innerHTML = '';
            this.emptyState.classList.remove('hidden');
            return;
        }

        this.emptyState.classList.add('hidden');
        this.todoList.innerHTML = filteredTodos.map(todo => this.createTodoElement(todo)).join('');

        // Add event listeners to rendered elements
        this.todoList.querySelectorAll('.checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                this.toggleTodo(parseInt(e.target.dataset.id));
            });
        });

        this.todoList.querySelectorAll('.btn-edit').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.editTodo(parseInt(e.target.dataset.id));
            });
        });

        this.todoList.querySelectorAll('.btn-delete').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.deleteTodo(parseInt(e.target.dataset.id));
            });
        });
    }

    // Create todo element HTML
    createTodoElement(todo) {
        const completedClass = todo.completed ? 'completed' : '';
        return `
            <div class="todo-item ${completedClass}">
                <input 
                    type="checkbox" 
                    class="checkbox" 
                    data-id="${todo.id}"
                    ${todo.completed ? 'checked' : ''}
                />
                <div class="todo-text">${todo.text}</div>
                <div class="todo-time">${this.formatTime(todo.updatedAt)}</div>
                <div class="todo-actions">
                    <button class="btn-edit" data-id="${todo.id}">Edit</button>
                    <button class="btn-delete" data-id="${todo.id}">Delete</button>
                </div>
            </div>
        `;
    }

    // Format time
    formatTime(dateStr) {
        const date = new Date(dateStr);
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);

        if (date.toDateString() === today.toDateString()) {
            return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
        } else if (date.toDateString() === yesterday.toDateString()) {
            return 'Yesterday';
        } else {
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        }
    }

    // Escape HTML to prevent XSS
    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    // Unescape HTML
    unescapeHtml(text) {
        const map = {
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&quot;': '"',
            '&#039;': "'"
        };
        return text.replace(/&amp;|&lt;|&gt;|&quot;|&#039;/g, m => map[m]);
    }

    // Show notification
    showNotification(message, type = 'info') {
        // Simple notification using console (can be enhanced with toast)
        console.log(`[${type.toUpperCase()}] ${message}`);
        
        // Optional: Create visual toast notification
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: ${type === 'success' ? '#4caf50' : type === 'error' ? '#f44336' : '#2196f3'};
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            font-weight: 500;
            z-index: 999;
            animation: slideInToast 0.3s ease-out;
        `;
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity 0.3s ease-out';
            setTimeout(() => document.body.removeChild(toast), 300);
        }, 3000);
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new TodoApp();
});

// Add toast animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInToast {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);