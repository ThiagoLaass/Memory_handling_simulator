const MAIN_MEMORY_LIMIT = 10;
const VIRTUAL_MEMORY_LIMIT = 15;
const TOTAL_PROCESSES = 8;
const PAGE_SIZE = 2;

class Frame {
    constructor(page) {
        this.page = page;
        this.lastAccessTime = 0;
    }
}

class Process {
    constructor(id, executionTime, arrivalTime) {
        this.id = id;
        this.executionTime = executionTime;
        this.remainingTime = executionTime;
        this.arrivalTime = arrivalTime;
        this.pages = Array(Math.ceil(executionTime / PAGE_SIZE)).fill({}).map((_, i) => ({
            pageId: `${id}-P${i + 1}`,
            remainingTime: Math.min(PAGE_SIZE, executionTime - i * PAGE_SIZE),
            inMainMemory: false
        }));
    }
}

let processes = [];
let mainMemory = [];
let virtualMemory = [];
let currentTime = 0;
let simulationInterval;

function startSimulation() {
    generateProcessesAsync();
    simulationInterval = setInterval(runSJF, 1000);
}

async function generateProcessesAsync() {
    for (let i = 0; i < TOTAL_PROCESSES; i++) {
        await new Promise(resolve => setTimeout(resolve, Math.random() * 1000 + 500));
        createProcess(i);
    }
}

function createProcess(index) {
    let executionTime = Math.floor(Math.random() * 8) + 2;
    let arrivalTime = currentTime;
    let process = new Process(`P${index + 1}`, executionTime, arrivalTime);

    logStatus(`Criado ${process.id} com tempo de execução ${executionTime} e ${process.pages.length} páginas`);

    process.pages.forEach(page => {
        if (mainMemory.length < MAIN_MEMORY_LIMIT) {
            let frame = new Frame(page);
            mainMemory.push(frame);
            page.inMainMemory = true;
            renderMemory();
            logStatus(`Página ${page.pageId} de ${process.id} alocada na memória principal`);
        } else {
            applyLRU(page);
        }
    });
}

function applyLRU(newPage) {
    let lruFrame = mainMemory.reduce((leastUsed, frame) => frame.lastAccessTime < leastUsed.lastAccessTime ? frame : leastUsed);
    
    logStatus(`Memória cheia. Movendo ${lruFrame.page.pageId} para memória virtual (LRU)`);
    mainMemory = mainMemory.filter(frame => frame !== lruFrame);
    virtualMemory.push(lruFrame.page);
    lruFrame.page.inMainMemory = false;

    let newFrame = new Frame(newPage);
    mainMemory.push(newFrame);
    newPage.inMainMemory = true;
    renderMemory();
    logStatus(`Página ${newPage.pageId} alocada na memória principal`);
}

function runSJF() {
    currentTime++;

    let runnableFrames = mainMemory.filter(frame => frame.page.remainingTime > 0);

    if (runnableFrames.length === 0 && virtualMemory.length > 0) {
        const loadedPage = loadPageToMainMemory();
        if (loadedPage) {
            runnableFrames.push(new Frame(loadedPage));
        }
    }

    let frameToRun = runnableFrames.length > 0
        ? runnableFrames.reduce((shortest, frame) =>
            (frame.page.remainingTime < shortest.page.remainingTime ? frame : shortest),
            { page: { remainingTime: Infinity } }
        )
        : null;

    if (!frameToRun) {
        logStatus(`Tempo ${currentTime}: Nenhuma página disponível para execução`);
        renderCPU(null);
        return;
    }

    frameToRun.page.remainingTime--;
    frameToRun.lastAccessTime = currentTime;
    renderCPU(frameToRun.page);
    logStatus(`Tempo ${currentTime}: Executando ${frameToRun.page.pageId} na CPU, tempo restante da página ${frameToRun.page.remainingTime}`);
    renderMemory();

    if (frameToRun.page.remainingTime === 0) {
        logStatus(`Tempo ${currentTime}: ${frameToRun.page.pageId} finalizou`);
        mainMemory = mainMemory.filter(frame => frame !== frameToRun);
        renderMemory();

        if (virtualMemory.length > 0) {
            loadPageToMainMemory();
        }
    }
}

function loadPageToMainMemory() {
    if (virtualMemory.length === 0) return null;

    let pageToLoad = virtualMemory.shift();
    pageToLoad.inMainMemory = true;

    if (mainMemory.length >= MAIN_MEMORY_LIMIT) {
        let lruFrame = mainMemory.reduce((leastUsed, frame) => 
            frame.lastAccessTime < leastUsed.lastAccessTime ? frame : leastUsed
        );

        logStatus(`Memória cheia. Substituindo ${lruFrame.page.pageId} por ${pageToLoad.pageId} (LRU)`);
        mainMemory = mainMemory.filter(frame => frame !== lruFrame);
        virtualMemory.push(lruFrame.page);
        lruFrame.page.inMainMemory = false;
    }

    let frameToLoad = new Frame(pageToLoad);
    mainMemory.push(frameToLoad);
    renderMemory();
    logStatus(`Página ${frameToLoad.page.pageId} carregada para a memória principal`);
    return frameToLoad.page;
}

function renderCPU(page) {
    const cpuDiv = document.getElementById('cpu');
    cpuDiv.innerHTML = page ? `<p>Executando: ${page.pageId} (Tempo restante: ${page.remainingTime})</p>` : `<p>CPU ociosa</p>`;
}

function renderMemory() {
    const mainMemoryDiv = document.getElementById('main-memory');
    mainMemoryDiv.innerHTML = '';
    for (let i = 0; i < MAIN_MEMORY_LIMIT; i++) {
        const frame = mainMemory[i];
        const cell = document.createElement('div');
        cell.className = `memory-cell ${frame ? 'memory-cell-main' : 'memory-cell-empty'}`;
        cell.innerText = frame ? `${frame.page.pageId} (T${frame.page.remainingTime})` : 'Vazio';
        mainMemoryDiv.appendChild(cell);
    }

    const virtualMemoryDiv = document.getElementById('virtual-memory');
    virtualMemoryDiv.innerHTML = '';
    for (let i = 0; i < VIRTUAL_MEMORY_LIMIT; i++) {
        const page = virtualMemory[i];
        const cell = document.createElement('div');
        cell.className = `memory-cell ${page ? 'memory-cell-virtual' : 'memory-cell-empty'}`;
        cell.innerText = page ? `${page.pageId} (T${page.remainingTime})` : 'Vazio';
        virtualMemoryDiv.appendChild(cell);
    }
}

function logStatus(message) {
    const logDiv = document.getElementById('status-log');
    logDiv.innerHTML += `<p>${message}</p>`;
    logDiv.scrollTop = logDiv.scrollHeight;
}
