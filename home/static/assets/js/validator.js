
const allowedExecutables = [
    'echo', 'ls', 'cat', 'mkdir', 'rm', 'cp', 'mv', 'touch', 'chmod', 'chown',
    'pwd', 'cd', 'ln', 'find', 'grep', 'awk', 'sed', 'sort', 'tar', 'gzip',
    'unzip', 'du', 'df', 'hostname', 'date', 'whoami', 'ps', 'kill', 'ping',
    'traceroute', 'ifconfig','curl', 'wget', 'git', 'svn', 'ssh', 'scp', 'rsync', 'apt-get',
    'ping', 'netstat', 'nmap', 'telnet', 'dig', 'host', 'nslookup', 'ssh-keygen',
    'openssl', 'pgrep', 'pkill', 'ps', 'pstree', 'killall', 'uptime', 'watch', 'free',
    'top', 'htop', 'iotop', 'iftop', 'ss', 'lsof', 'strace', 'tcpdump', 'wireshark',
    'vmstat', 'iostat', 'sar', 'mpstat', 'pidstat', 'dstat', 'atop', 'at', 'crontab',
    'systemctl', 'service', 'chkconfig', 'journalctl', 'lsmod', 'modinfo', 'modprobe',
    'insmod', 'rmmod', 'lsusb', 'lspci', 'lsblk', 'fdisk', 'gdisk', 'parted', 'mkfs',
    'mount', 'umount', 'df', 'du', 'fdisk', 'fsck', 'badblocks', 'smartctl', 'dd',
    'head', 'tail', 'less', 'more', 'file', 'diff', 'wc', 'cut', 'paste', 'join',
    'comm', 'uniq', 'tr', 'wc', 'split', 'xargs', 'tee', 'seq', 'yes', 'bc', 'expr',
    'factor', 'bc', 'dc', 'units', 'uptime', 'date', 'cal', 'bc', 'dc', 'units',
    'uptime', 'date', 'cal', 'bc', 'dc', 'units', 'uname', 'hostname', 'dmesg',
    'lsmod', 'modinfo', 'modprobe', 'insmod', 'rmmod', 'lsusb', 'lspci', 'lsblk',
    "apt-install", "apt-remove", "apt-update", "apt-upgrade", "apt-search", "apt-show",
    "apt-list", "apt-add-repository", "apt-repository", "apt-mark", "apt-cache", "apt-file",
    'sudo', 'su', 'chroot', 'passwd', 'useradd', 'userdel', 'usermod', 'groupadd',
    'groupdel', 'groupmod', 'chown', 'chgrp', 'chmod', 'passwd', 'mkpasswd', 'mkgroup',
    'mkhomedir_helper', 'login', 'logout', 'exit', 'shutdown', 'reboot', 'halt', 'poweroff',
    'init', 'runlevel', 'telinit', 'systemd', 'systemctl', 'service', 'chkconfig',
    'journalctl', 'ps', 'top', 'htop', 'iotop', 'atop', 'uptime', 'w', 'who', 'last',
    'finger', 'id', 'groups', 'users', 'w', 'who', 'last', 'finger', 'id', 'groups',
    'users', 'w', 'who', 'last', 'finger', 'id', 'groups', 'users', 'w', 'who', 'last',
];

function removeFirstAndLastChar(str) {
    // Verificăm dacă șirul are lungimea mai mare de 1 pentru a asigura că avem ce elimina
    if (str.length > 1) {
        // console.log(str.substring(1, str.length - 1));
        return str.substring(2, str.length - 1); // Returnăm șirul fără primul și ultimul caracter
    } else {
        return str; // Dacă șirul are lungimea 1 sau mai mică, nu facem modificări
    }
}

function createArrayFromCsv(csvString) {
    // Împarte șirul după virgulă, eliminând spațiile în exces
    const elements = csvString.split(',').map(item => item.trim());
    
    // Elimină ghilimelele duble de la început și sfârșitul fiecărui element
    for (let i = 0; i < elements.length; i++) {
        elements[i] = removeFirstAndLastChar(elements[i]);
    }
    return elements;
}



function isValidPath(path) {
    // Exemplu simplificat: verifica dacă calea conține caractere valide
    // Acesta este doar un exemplu, trebuie adaptat pentru nevoile tale specifice
    const validChars = /^[a-zA-Z0-9\-_\/.* ]+$/;
    return validChars.test(path);
}

function validateArg(value) {
    // Verificăm dacă valoarea începe cu o literă și conține doar caractere alfanumerice și underscore
    if(value.trim() === '' || value === null) {
        return true;
    }
    const validRegex = /^[a-zA-Z0-9_]*(?:=[a-zA-Z0-9_]+)?$/;
    return validRegex.test(value);
}

// Funcție pentru a valida instrucțiunea ADD
function validateAdd(value) {
    console.log('space');
    if(value.trim() === '' || value === null) {
        return true;
    }

    // Verificăm dacă valoarea conține exact două argumente separate prin spațiu
    const firstSpaceIndex = value.indexOf(' ');
    if (firstSpaceIndex === -1) {
        // If there's no space, it's an invalid format for ADD instruction
        console.log('no space');
        return false;
    }

    // Separate source and destination paths
    const source = value.substring(0, firstSpaceIndex);
    const destination = value.substring(firstSpaceIndex + 1);
    console.log(source);
    // Validate the paths
    if (!isValidPath(source) || !isValidPath(destination)) {
        console.log('path invalid');
        return false;
    }

    if (!isValidPath(source) || !isValidPath(destination)) {
        console.log('space');
        return false;
    }

    // Aici poți adăuga și alte verificări, cum ar fi existența căilor pe sistemul de fișiere

    return true;
}

function validateCopy(value) {

    if(value.trim() === '' || value === null) {
        return true;
    }

    // Verificăm dacă valoarea conține exact două argumente separate prin spațiu
    const parts = value.trim().split(/\s+/);
    if (parts.length !== 2) {
        return false;
    }

    // Verificăm validitatea căilor de sursă și destinație
    const source = parts[0];
    const destination = parts[1];

    if (!isValidPath(source) || !isValidPath(destination)) {
        return false;
    }

    // Aici poți adăuga și alte verificări, cum ar fi existența căilor pe sistemul de fișiere

    return true;
}

function validateCmd(cmd) {
    if(cmd.trim() === '' || cmd === null) {
        return true;
    }


    // Function to check if a string is a valid executable name
    function isValidExecutable(executable) {
        // List of allowed executables (for demonstration)
        return allowedExecutables.includes(executable);
    }

    // Function to validate the exec form of CMD instruction
    function validateExecForm(cmdArray) {
        
        if (cmdArray.length > 0) {
            // First element should be the executable name (command)
            cmdArray = createArrayFromCsv(cmdArray);
            console.log(cmdArray);
            const executable = cmdArray[0];
            console.log(executable);
            // Check if the executable is valid
            if (isValidExecutable(executable)) {
                // Additional validation for parameters (if any)
                // Assuming any array with valid executable is valid for demo
                return true;
            }
        }
        return false;
    }

    // Function to validate the shell form of CMD instruction
    function validateShellForm(cmdString) {
        // Check if cmdString is a non-empty string
        if (typeof cmdString === 'string' && cmdString.trim().length > 0) {
            // Split the command string into parts (command and parameters)
            const parts = cmdString.trim().split(/\s+/);
            // Check if there are at least two parts (command and at least one parameter)
            if (parts.length >= 2) {
                // First part is the command
                const command = parts[0];
                // Check if the command is a valid executable
                if (isValidExecutable(command)) {
                    return true;
                }
            }
            else if(parts.length === 1) {
                if (isValidExecutable(cmdString)) {
                    return true;
                }
            }
        }
        return false;
    }

    // Check if cmd is an array (exec form)
    if (cmd.startsWith('[') && cmd.endsWith(']')){
        console.log('exec form');
        return validateExecForm(cmd); // Return the result of validateExecForm
    }

    // Check if cmd is a string (shell form)
    if (typeof cmd === 'string') {
        console.log('shell form');
        return validateShellForm(cmd);
    }
    console.log('invalid');

    // If cmd is neither an array nor a string, it's invalid
    return false;
}





function validateEntrypoint(value) {
    // Verificăm dacă valoarea nu este goală și nu conține caractere de linie nouă
    return validateCmd(value);
}

function validateEnv(value) {

    // Verificăm dacă valoarea respectă formatul key=value
    if(value.trim() === '' || value === null) {
        return true;
    }

    const keyValueRegex = /(([a-zA-Z_][a-zA-Z0-9_]*)=([^\\ ]*(?:\\ [^\\ ]*)*))+$/;
    if (!keyValueRegex.test(value.trim())) {
        return false;
    }

    // Poți adăuga și alte verificări specifice pentru sintaxa ENV

    return true;
}

function validateExpose(value) {

    if(value.trim() === '' || value === null) {
        return true;
    }

    // Verificăm dacă valoarea conține doar numere întregi separate prin virgulă
    const portRegex = /^\s*(\d+)\s*(?:\s*,\s*(\d+)\s*)*$/;
    if (!portRegex.test(value.trim())) {
        return false;
    }

    // Verificăm dacă fiecare port este în intervalul valid (1-65535)
    const ports = value.trim().split(/\s*,\s*/).map(port => parseInt(port, 10));
    for (let port of ports) {
        if (port < 1 || port > 65535) {
            return false;
        }
    }

    return true;
}


function validateHealthcheck(value) {

    if(value.trim() === '' || value === null) {
        return true;
    }

    // Verificăm dacă valoarea începe cu una din opțiunile suportate (none, CMD, HEALTHCHECK)
    const supportedOptions = [/^CMD/, /^HEALTHCHECK/, /^NONE/, /^--interval=.*/, /^--timeout=.*/, /^--start-period=.*/, /^--retries=.*/];    let isValidOption = false;
    for (let option of supportedOptions) {
        if (option.test(value.trim()))    {
            isValidOption = true;
            break;
        }
    }
    if (!isValidOption) {
        return false;
    }

    // Verificăm dacă valoarea respectă formatul specificat pentru opțiunea CMD sau HEALTHCHECK
    if (value.trim().startsWith('CMD')) {
        // Opțiunea CMD: HEALTHCHECK CMD command
        const cmdRegex = /^CMD\s+(.+)\s*$/;
        const match = value.trim().match(cmdRegex);

    if (match) {
        // match[1] conține textul după "CMD"
        const textAfterCmd = match[1];
        console.log(textAfterCmd);
        return validateCmd(textAfterCmd);
    }
    } else if (value.trim().startsWith('HEALTHCHECK')) {
        // Opțiunea HEALTHCHECK: HEALTHCHECK [--interval=DURATION] [--timeout=DURATION] \
        //   [--start-period=DURATION] [--retries=N] CMD command
        const healthcheckRegex = /^HEALTHCHECK\s+((--interval=\d+[mhs]?|--timeout=\d+[mhs]?|--start-period=\d+[mhs]?|--retries=\d+\s+)?)*CMD\s+.+\s*$/;
        if (!healthcheckRegex.test(value.trim())) {
            return false;
        }
    }

    else if (value.trim().startsWith('NONE')) {
        return value === 'NONE';
    }

    return true;
}


function validateLabel(value) {

    return validateEnv(value);
}

function validateOnbuild(value) {
    if(value.trim() === '' || value === null) {
        return true;
    }


    // Verificăm dacă valoarea nu este goală și nu conține caractere de linie nouă
    if (value.includes('\n') || value.includes('\r')) {
        return false;
    }

    // Verificăm dacă valoarea începe cu o comandă shell validă
    // Se acceptă comenzi shell simple și unele opțiuni frecvent utilizate în Docker pentru ONBUILD
    const allowedDockerfileCommands = ['ADD', 'COPY', 'ENV', 'EXPOSE', 'FROM', 'HEALTHCHECK', 'LABEL', 'MAINTAINER', 'RUN', 'SHELL', 'STOPSIGNAL', 'USER', 'VOLUME', 'WORKDIR'];
    let validShellCommand = false;
    for (let command of allowedDockerfileCommands) {
        if (value.trim().startsWith(command)) {
            switch (command) {
                case 'RUN':
                    isValid = validateRun(value);
                    break;
                case 'CMD':
                    isValid = validateCmd(value);
                    break;
                case 'LABEL':
                    isValid = validateLabel(value);
                    break;
                case 'MAINTAINER':
                    isValid = validateMaintainer(value); // Note: 'MAINTAINER' is deprecated in favor of 'LABEL'
                    break;
                case 'EXPOSE':
                    isValid = validateExpose(value);
                    break;
                case 'ENV':
                    isValid = validateEnv(value);
                    break;
                case 'ADD':
                    isValid = validateAdd(value);
                    break;
                case 'COPY':
                    isValid = validateCopy(value);
                    break;
                case 'ENTRYPOINT':
                    isValid = validateEntrypoint(value);
                    break;
                case 'VOLUME':
                    isValid = validateVolume(value);
                    break;
                case 'USER':
                    isValid = validateUser(value);
                    break;
                case 'WORKDIR':
                    isValid = validateWorkdir(value);
                    break;
                case 'ARG':
                    isValid = validateArg(value);
                    break;
                case 'ONBUILD':
                    isValid = validateOnbuild(value);
                    break;
                case 'STOPSIGNAL':
                    isValid = validateStopsignal(value);
                    break;
                case 'HEALTHCHECK':
                    isValid = validateHealthcheck(value);
                    break;
                case 'SHELL':
                    isValid = validateShell(value);
                    break;
                default:
                        isValid = true; // Default to true if no specific validation is needed
                        break;
                }
            return isValid;
        }
    }
    if (!validShellCommand) {
        return false;
    }

    // Verificăm dacă comanda respectă o sintaxă simplificată pentru Docker (opțional)
    // Poți adăuga verificări suplimentare pentru a asigura o sintaxă validă pentru Docker pentru ONBUILD
    const parts = value.trim().split(/\s+/);
    if (parts.length < 2) {
        return false;
    }

    // Poți adăuga și alte verificări specifice pentru sintaxa Docker pentru ONBUILD

    return true;
}

function validateRun(value) {

    if(value.trim() === '' || value === null) {
        return true;
    }

    const options = ['--mount', '--network', '--security']
    const words = value.split(' ');

// Primul cuvânt este primul element din array-ul words
    const first = words[0];

    for (let command of allowedExecutables) {
        if (value.trim().startsWith(command)) {
            validShellCommand = true;
            break;
        }
    }

    for (let option of options) {
        if (value.trim().startsWith(option)) {
            validShellCommand = true;
            break;
        }
    }

    // Verificăm dacă textul conține cel puțin un spațiu urmat de conținut
    if (!/\s+.+/.test(value)) {
        return false;
    }

    // Verificăm dacă textul conține caracterul '\' urmat de linie nouă, semn că comanda continuă pe mai multe linii
    if (value.includes('\\\n')) {
        return false;
    }

    // Verificăm dacă textul conține caractere nepermise care ar putea sugera un atac de tip injection
    const forbiddenChars = /[;&|<>]/;
    if (forbiddenChars.test(value)) {
        return false;
    }

    // Dacă trece toate verificările, comanda este considerată validă
    return validShellCommand;
}

function validateShell(value) {

    const executables = ['bash', 'sh', 'zsh', 'powershell', 'cmd'];
    const cmdArray = createArrayFromCsv(value);
    // Verificăm dacă value este un array și are cel puțin două elemente
    // if (value.length < 2) {
    //     return false;
    // }
    if(!value.startsWith('[') && !value.endsWith(']')) {
        return false;
    }
    // Verificăm primul element (executable)
    const executable = cmdArray[0];
    if (!executables.includes(executable)) {
        console.log(executable);
        return false;
    }
    // console.log(value);

    // Dacă toate condițiile sunt îndeplinite, returnăm true
    return true;
}

function validateStopsignal(value) {

    if(value.trim() === '' || value === null) {
        return true;
    }
    // Verificăm dacă valoarea nu este goală și nu conține caractere de linie nouă
    if (value.includes('\n') || value.includes('\r')) {
        return false;
    }

    // Verificăm dacă valoarea începe cu un semnal de stop valid
    // Se acceptă semnalele de stop standard conform specificațiilor Docker
    const allowedSignals = ['SIGABRT', 'SIGALRM', 'SIGBUS', 'SIGCHLD', 'SIGCONT', 'SIGFPE', 'SIGHUP', 'SIGILL', 'SIGINT', 'SIGIO', 'SIGIOT', 'SIGKILL', 'SIGPIPE', 'SIGPOLL', 'SIGPROF', 'SIGPWR', 'SIGQUIT', 'SIGSEGV', 'SIGSTKFLT', 'SIGSTOP', 'SIGSYS', 'SIGTERM', 'SIGTRAP', 'SIGTSTP', 'SIGTTIN', 'SIGTTOU', 'SIGUNUSED', 'SIGURG', 'SIGUSR1', 'SIGUSR2', 'SIGVTALRM', 'SIGWINCH', 'SIGXCPU', 'SIGXFSZ'];
    
    if (!allowedSignals.includes(value.trim())) {
        return false;
    }

    // Returnăm true dacă trece toate verificările
    return true;
}

function validateUser(value) {
    if(value.trim() === '' || value === null) {
        return true;
    }
    // Verificăm dacă valoarea nu este goală și nu conține caractere de linie nouă
    if (value.includes('\n') || value.includes('\r')) {
        return false;
    }

    // Verificăm dacă valoarea respectă o formă simplificată pentru un nume de utilizator Unix
    // Exemplu simplificat: trebuie să conțină doar litere mici, cifre și caracterul underscore (_)
    if (!/^[a-z0-9_]*(:([a-z0-9_])+)?$/i.test(value.trim())) {
        return false;
    }

    // Returnăm true dacă trece toate verificările
    return true;
}


function validateVolume(value) {

    if(value.trim() === '' || value === null) {
        return true;
    }
    if(value.startsWith('[')){
        if(!value.endsWith(']')) {
            return false;
        }
    }

    if(value.startsWith('[')){
        value = removeFirstAndLastChar(value);
        value = value.substring(1, value.length - 2);
        return isValidPath(value);
    }
    // Verificăm dacă valoarea nu este goală și nu conține caractere de linie nouă
    if (!value.trim() || value.includes('\n') || value.includes('\r')) {
        return false;
    }

    // Verificăm dacă valoarea este un director valid într-un format simplificat
    // Exemplu simplificat: trebuie să înceapă cu / și poate conține litere, cifre, cratimă și underscore
    if (!isValidPath(value.trim())) {
        return false;
    }

    // Returnăm true dacă trece toate verificările
    return true;
}

function validateWorkdir(value) {
    if(value.trim() === '' || value === null) {
        return true;
    }
    // Verificăm dacă valoarea nu este goală și nu conține caractere de linie nouă
    if (!value.trim() || value.includes('\n') || value.includes('\r')) {
        return false;
    }

    // Verificăm dacă valoarea este un director valid într-un format simplificat
    // Exemplu simplificat: trebuie să înceapă cu / și poate conține litere, cifre, cratimă și underscore
    if (!isValidPath(value.trim())) {
        return false;
    }

    // Returnăm true dacă trece toate verificările
    return true;
}