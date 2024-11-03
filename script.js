const MAIN_MEMORY_LIMIT = 10; // Número de células de memória na memória principal
const VIRTUAL_MEMORY_LIMIT = 15; // Número de células de memória na memória virtual
const TOTAL_PROCESSES = 8; // Total de processos a serem criados dinamicamente
const PAGE_SIZE = 2; // Número de "páginas" ou células por processo

class Process {
  constructor(id, executionTime, arrivalTime) {
    this.id = id;
    this.executionTime = executionTime;
    this.remainingTime = executionTime;
    this.arrivalTime = arrivalTime;
    this.pages = Array(Math.ceil(executionTime / PAGE_SIZE)).fill({}).map((_, i) => ({
      pageId: `${id}-P${i + 1}`,
      remainingTime: Math.min(PAGE_SIZE, executionTime - i * PAGE_SIZE),
      inMainMemory: false,
    }));
  }
}

let processes = [];
let mainMemory = [];
let virtualMemory = [];
let currentTime = 0;

function startSimulation() {
  generateProcessesAsync();
  setInterval(runSJF, 1000);
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
      mainMemory.push(page);
      page.inMainMemory = true;
      renderMemory();
      logStatus(`Página ${page.pageId} de ${process.id} alocada na memória principal`);
    } else {
      virtualMemory.push(page);
      renderMemory();
      logStatus(`Página ${page.pageId} de ${process.id} movida para a memória virtual`);
    }
  });
}

function runSJF() {
  currentTime++;
  
  let pageToRun = mainMemory.reduce((shortest, p) => (p.remainingTime < shortest.remainingTime ? p : shortest), { remainingTime: Infinity });
  
  if (pageToRun && pageToRun.remainingTime > 0) {
    pageToRun.remainingTime--;
    logStatus(`Tempo ${currentTime}: Executando ${pageToRun.pageId}, tempo restante da página ${pageToRun.remainingTime}`);
    renderMemory();

    if (pageToRun.remainingTime === 0) {
      logStatus(`Tempo ${currentTime}: ${pageToRun.pageId} finalizou`);
      mainMemory = mainMemory.filter(p => p !== pageToRun);
      renderMemory();

      if (virtualMemory.length > 0) {
        let nextPage = virtualMemory.shift();
        nextPage.inMainMemory = true;
        mainMemory.push(nextPage);
        renderMemory();
        logStatus(`Página ${nextPage.pageId} movida da memória virtual para a memória principal`);
      }
    }
  } else {
    logStatus(`Tempo ${currentTime}: Nenhuma página disponível para execução`);
  }
}

function renderMemory() {
  const mainMemoryDiv = document.getElementById('main-memory');
  mainMemoryDiv.innerHTML = '';
  for (let i = 0; i < MAIN_MEMORY_LIMIT; i++) {
    const page = mainMemory[i];
    const cell = document.createElement('div');
    cell.className = `memory-cell ${page ? 'memory-cell-main' : 'memory-cell-empty'}`;
    cell.innerText = page ? `${page.pageId} (T${page.remainingTime})` : 'Vazio';
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
