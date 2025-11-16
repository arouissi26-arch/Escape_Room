// Planificador de Exámenes con IA - Frontend
// Comunicación con backend Flask

const API_URL = window.location.origin;

// Estado de la aplicación
let flashcards = [];
let exams = [];

// Elementos del DOM
const contentInput = document.getElementById('contentInput');
const generateBtn = document.getElementById('generateBtn');
const loading = document.getElementById('loading');
const flashcardsContainer = document.getElementById('flashcardsContainer');
const examsList = document.getElementById('examsList');
const addExamBtn = document.getElementById('addExamBtn');
const clearBtn = document.getElementById('clearBtn');
const fileUpload = document.getElementById('fileUpload');
const fileInput = document.getElementById('fileInput');

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    loadData();
    updateStats();
    setupEventListeners();
});

// Configurar event listeners
function setupEventListeners() {
    generateBtn.addEventListener('click', generateFlashcards);
    addExamBtn.addEventListener('click', addExam);
    clearBtn.addEventListener('click', clearFlashcards);

    // File upload
    fileUpload.addEventListener('click', () => fileInput.click());

    fileUpload.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUpload.style.borderColor = 'var(--accent-gold)';
    });

    fileUpload.addEventListener('dragleave', () => {
        fileUpload.style.borderColor = 'var(--border-color)';
    });

    fileUpload.addEventListener('drop', (e) => {
        e.preventDefault();
        fileUpload.style.borderColor = 'var(--border-color)';
        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });
}

// Manejar archivo subido
function handleFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        contentInput.value = e.target.result;
        showNotification(`Archivo cargado: ${file.name}`);
    };
    reader.readAsText(file);
}

// Generar flashcards con IA
async function generateFlashcards() {
    const content = contentInput.value.trim();

    if (!content) {
        showNotification('Por favor, ingresa contenido primero', 'error');
        return;
    }

    // Mostrar loading
    loading.classList.add('active');
    generateBtn.disabled = true;

    try {
        const response = await fetch(`${API_URL}/api/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content })
        });

        if (!response.ok) {
            throw new Error('Error en la generación');
        }

        const data = await response.json();

        if (data.success) {
            flashcards = [...flashcards, ...data.flashcards];
            saveData();
            displayFlashcards();
            updateStats();
            showNotification(`✓ ${data.count} tarjetas generadas exitosamente`);

            if (flashcards.length > 0) {
                clearBtn.style.display = 'block';
            }
        }

    } catch (error) {
        console.error('Error:', error);
        showNotification('Error al generar tarjetas. Verifica que el servidor esté corriendo.', 'error');
    } finally {
        loading.classList.remove('active');
        generateBtn.disabled = false;
    }
}

// Mostrar flashcards
function displayFlashcards() {
    if (flashcards.length === 0) {
        flashcardsContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">🎴</div>
                <p>No hay tarjetas generadas aún</p>
                <p class="small">Sube contenido y genera tarjetas con IA</p>
            </div>
        `;
        clearBtn.style.display = 'none';
        return;
    }

    flashcardsContainer.innerHTML = flashcards.map((card, index) => `
        <div class="flashcard" onclick="toggleFlashcard(this)">
            <div class="flashcard-type">${card.type}</div>
            <div class="flashcard-number">${index + 1}</div>
            <div class="flashcard-question">❓ ${card.question}</div>
            <div class="flashcard-answer">💡 ${card.answer}</div>
            <div class="flashcard-difficulty">${getDifficultyIcon(card.difficulty)} ${card.difficulty}</div>
        </div>
    `).join('');

    clearBtn.style.display = 'block';
}

// Voltear flashcard
function toggleFlashcard(element) {
    element.classList.toggle('flipped');
}

// Icono de dificultad
function getDifficultyIcon(difficulty) {
    const icons = {
        'fácil': '🟢',
        'medio': '🟡',
        'difícil': '🔴'
    };
    return icons[difficulty] || '⚪';
}

// Limpiar flashcards
function clearFlashcards() {
    if (confirm('¿Estás seguro de que quieres borrar todas las tarjetas?')) {
        flashcards = [];
        saveData();
        displayFlashcards();
        updateStats();
        showNotification('Tarjetas eliminadas');
    }
}

// Agregar examen
function addExam() {
    const exam = {
        id: Date.now(),
        subject: '',
        date: '',
        time: ''
    };
    exams.push(exam);
    saveData();
    displayExams();
    updateStats();
}

// Eliminar examen
function removeExam(id) {
    exams = exams.filter(e => e.id !== id);
    saveData();
    displayExams();
    updateStats();
}

// Actualizar examen
function updateExam(id, field, value) {
    const exam = exams.find(e => e.id === id);
    if (exam) {
        exam[field] = value;
        saveData();
        updateStats();
    }
}

// Mostrar exámenes
function displayExams() {
    if (exams.length === 0) {
        examsList.innerHTML = '<p class="empty-state">No hay exámenes programados</p>';
        return;
    }

    examsList.innerHTML = exams.map(exam => `
        <div class="exam-item">
            <input type="text"
                   placeholder="Asignatura (ej: Matemáticas)"
                   value="${exam.subject || ''}"
                   onchange="updateExam(${exam.id}, 'subject', this.value)">
            <input type="date"
                   value="${exam.date || ''}"
                   onchange="updateExam(${exam.id}, 'date', this.value)">
            <input type="time"
                   value="${exam.time || ''}"
                   onchange="updateExam(${exam.id}, 'time', this.value)">
            <button onclick="removeExam(${exam.id})">Eliminar</button>
        </div>
    `).join('');
}

// Actualizar estadísticas
function updateStats() {
    document.getElementById('totalCards').textContent = flashcards.length;
    document.getElementById('totalExams').textContent = exams.length;

    // Calcular días hasta el próximo examen
    const upcomingExams = exams
        .filter(e => e.date)
        .map(e => ({ ...e, dateObj: new Date(e.date) }))
        .filter(e => e.dateObj >= new Date())
        .sort((a, b) => a.dateObj - b.dateObj);

    if (upcomingExams.length > 0) {
        const days = Math.ceil((upcomingExams[0].dateObj - new Date()) / (1000 * 60 * 60 * 24));
        document.getElementById('daysToExam').textContent = days;
    } else {
        document.getElementById('daysToExam').textContent = '-';
    }
}

// Guardar datos en localStorage
function saveData() {
    localStorage.setItem('flashcards', JSON.stringify(flashcards));
    localStorage.setItem('exams', JSON.stringify(exams));
}

// Cargar datos de localStorage
function loadData() {
    const savedFlashcards = localStorage.getItem('flashcards');
    if (savedFlashcards) {
        flashcards = JSON.parse(savedFlashcards);
        displayFlashcards();
    }

    const savedExams = localStorage.getItem('exams');
    if (savedExams) {
        exams = JSON.parse(savedExams);
        displayExams();
    }
}

// Mostrar notificación
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = 'notification show';

    if (type === 'error') {
        notification.style.background = 'var(--error)';
        notification.style.color = 'white';
    } else {
        notification.style.background = 'var(--accent-gold)';
        notification.style.color = 'var(--primary-bg)';
    }

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Verificar estado del servidor
async function checkServerHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        console.log('✅ Servidor conectado:', data);
    } catch (error) {
        console.error('❌ Error de conexión con el servidor');
        showNotification('Error: Asegúrate de que el servidor Flask esté corriendo', 'error');
    }
}

// Verificar al cargar
checkServerHealth();
