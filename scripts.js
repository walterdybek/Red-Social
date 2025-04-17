// UFlow Daily System
const uflowBtn = document.getElementById('uflowBtn');
const uflowProgress = document.getElementById('uflowProgress');
const uflowCounter = document.getElementById('uflowCounter');
const uflowModal = document.getElementById('uflowModal');
const closeModal = document.getElementById('closeModal');
const uflowText = document.getElementById('uflowText');
const publishUflow = document.getElementById('publishUflow');
const charCounter = document.getElementById('charCounter');

let canPostUFlow = false;

function updateUFlowStatus() {
    const now = new Date();
    const today = new Date();
    today.setHours(23, 59, 59, 999);

    const timeLeft = today - now;

    if (timeLeft > 0) {
        const hours = Math.floor(timeLeft / (1000 * 60 * 60));
        const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

        uflowCounter.querySelector('span').textContent =
            `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        const lastUFlow = localStorage.getItem('lastUFlow');
        const lastDate = lastUFlow ? new Date(lastUFlow) : null;
        const isToday = lastDate && new Date().toDateString() === lastDate.toDateString();

        if (isToday) {
            uflowBtn.disabled = true;
            uflowProgress.style.width = `${((now.getHours() * 60 + now.getMinutes()) / (24 * 60)) * 100}%`;
            canPostUFlow = false;
            uflowCounter.querySelector('span').textContent = '¡Ya has publicado hoy!';
            uflowCounter.querySelector('span').style.color = 'var(--secondary)';
        } else {
            resetUFlow();
        }
    } else {
        resetUFlow();
    }
}

function resetUFlow() {
    uflowProgress.style.width = '0%';
    uflowCounter.querySelector('span').textContent = '¡Disponible!';
    uflowCounter.querySelector('span').style.color = 'var(--secondary)';
    uflowBtn.disabled = false;
    canPostUFlow = true;
}

uflowBtn.addEventListener('click', () => {
    if (canPostUFlow) {
        uflowModal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
});

closeModal.addEventListener('click', () => {
    uflowModal.classList.remove('active');
    document.body.style.overflow = 'auto';
});

uflowText.addEventListener('input', () => {
    const length = uflowText.value.length;
    charCounter.textContent = `${length}/280`;
    publishUflow.disabled = length === 0;
    
    if (length > 280) {
        charCounter.style.color = 'red';
    } else {
        charCounter.style.color = '#888';
    }
});

publishUflow.addEventListener('click', () => {
    if (uflowText.value.trim() === '') return;
    
    localStorage.setItem('lastUFlow', new Date().toISOString());
    uflowModal.classList.remove('active');
    document.body.style.overflow = 'auto';
    uflowText.value = '';
    charCounter.textContent = '0/280';
    
    gsap.to(uflowProgress, {
        width: '100%',
        duration: 0.5,
        ease: 'power2.out'
    });
    
    updateUFlowStatus();
});

// Pestañas
const tabs = document.querySelectorAll('.tab');
const contentGrid = document.getElementById('contentGrid');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        loadContent(tab.getAttribute('data-tab'));
    });
});

function loadContent(type) {
    contentGrid.innerHTML = '';
    
    let items = [];
    if (type === 'photos') {
        items = Array(9).fill().map((_, i) => ({
            type: 'image',
            url: `https://source.unsplash.com/random/300x300/?sig=${Math.floor(Math.random() * 1000)}`
        }));
    } else if (type === 'videos') {
        items = Array(6).fill().map((_, i) => ({
            type: 'video',
            url: `https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4`
        }));
    } else {
        items = Array(3).fill().map((_, i) => ({
            type: 'uflow',
            text: `Este es mi UFlow del día #${i+1}`
        }));
    }
    
    items.forEach(item => {
        const gridItem = document.createElement('div');
        gridItem.className = 'grid-item';
        
        if (item.type === 'image') {
            gridItem.innerHTML = `<img src="${item.url}" alt="Post">`;
        } else if (item.type === 'video') {
            gridItem.innerHTML = `
                <video muted loop>
                    <source src="${item.url}" type="video/mp4">
                </video>
                <i class="fas fa-play"></i>
            `;
        } else {
            gridItem.innerHTML = `
                <div class="uflow-content">
                    <p>${item.text}</p>
                    <i class="fas fa-bolt"></i>
                </div>
            `;
            gridItem.style.background = `linear-gradient(45deg, ${getRandomColor()}, ${getRandomColor()})`;
        }
        
        contentGrid.appendChild(gridItem);
    });
}

function getRandomColor() {
    const colors = ['#6E3AFF', '#FF3AC7', '#00FF9D', '#FF9D00'];
    return colors[Math.floor(Math.random() * colors.length)];
}

// Conexiones
function loadConnections() {
    const connectionsGrid = document.getElementById('connectionsGrid');
    connectionsGrid.innerHTML = '';
    
    Array(12).fill().forEach((_, i) => {
        const connection = document.createElement('div');
        connection.className = 'connection';
        connection.innerHTML = `
            <img src="https://i.pravatar.cc/80?img=${i+10}" alt="User">
        `;
        connectionsGrid.appendChild(connection);
    });
}

// Stats animados
function animateStats() {
    const stats = {
        likes: 14700,
        followers: 8300,
        following: 452
    };
    
    Object.keys(stats).forEach((stat) => {
        const element = document.getElementById(`${stat}Count`);
        const target = stats[stat];
        let current = 0;

        const increment = target / 30;
        const interval = setInterval(() => {
            current += increment;
            if (current >= target) {
                clearInterval(interval);
                element.textContent = target.toLocaleString();
                return;
            }
            element.textContent = Math.floor(current).toLocaleString();
        }, 20);
    });
}

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    updateUFlowStatus();
    setInterval(updateUFlowStatus, 1000);
    loadContent('photos');
    loadConnections();
    animateStats();
});