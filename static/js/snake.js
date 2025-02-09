class SnakeGame {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.BLOCK_SIZE = 20;
        this.playerName = localStorage.getItem('playerName') || 'Anonymous';
        
        this.snake = [];
        this.food = null;
        this.direction = 'RIGHT';
        this.score = 0;
        this.gameRunning = true;

        // Initialize gradients
        this.initGradients();
        
        // Bind event handlers
        this.handleKeyPress = this.handleKeyPress.bind(this);
        this.handleResize = this.handleResize.bind(this);
        
        // Add cleanup method binding
        this.cleanup = this.cleanup.bind(this);

        // Set up event listeners
        window.addEventListener('resize', this.handleResize);
        document.addEventListener('keydown', this.handleKeyPress);
        window.addEventListener('beforeunload', this.cleanup);
        
        // Initial setup
        this.setCanvasSize();
        this.init();
    }

    initGradients() {
        this.snakeGradient = this.ctx.createLinearGradient(0, 0, this.canvas.width, this.canvas.height);
        this.snakeGradient.addColorStop(0, '#00ff00');
        this.snakeGradient.addColorStop(1, '#008000');
    }

    setCanvasSize() {
        const vh = Math.min(window.innerHeight * 0.7, 480);
        const aspectRatio = 640/480;
        this.canvas.height = vh;
        this.canvas.width = vh * aspectRatio;
        this.initGradients(); // Reinitialize gradients after resize
    }

    handleResize() {
        this.setCanvasSize();
        if (this.gameRunning) {
            this.draw();
        }
    }

    init() {
        this.gameRunning = true;
        document.getElementById('gameOver').style.display = 'none';
        
        const startX = Math.floor(this.canvas.width / 2);
        const startY = Math.floor(this.canvas.height / 2);
        this.snake = [
            {x: startX, y: startY},
            {x: startX - this.BLOCK_SIZE, y: startY},
            {x: startX - (2 * this.BLOCK_SIZE), y: startY}
        ];
        this.placeFood();
        this.gameLoop();
    }

    placeFood() {
        const x = Math.floor(Math.random() * (this.canvas.width / this.BLOCK_SIZE)) * this.BLOCK_SIZE;
        const y = Math.floor(Math.random() * (this.canvas.height / this.BLOCK_SIZE)) * this.BLOCK_SIZE;
        this.food = {x, y};
    }

    handleKeyPress(event) {
        if (!this.gameRunning) return;
        
        const directionMap = {
            'ArrowUp': { allowed: this.direction !== 'DOWN', newDirection: 'UP' },
            'ArrowDown': { allowed: this.direction !== 'UP', newDirection: 'DOWN' },
            'ArrowLeft': { allowed: this.direction !== 'RIGHT', newDirection: 'LEFT' },
            'ArrowRight': { allowed: this.direction !== 'LEFT', newDirection: 'RIGHT' }
        };

        const newDirection = directionMap[event.key];
        if (newDirection && newDirection.allowed) {
            this.direction = newDirection.newDirection;
        }
    }

    moveSnake() {
        const head = {...this.snake[0]};
        const moveMap = {
            'UP': { y: -this.BLOCK_SIZE },
            'DOWN': { y: this.BLOCK_SIZE },
            'LEFT': { x: -this.BLOCK_SIZE },
            'RIGHT': { x: this.BLOCK_SIZE }
        };

        const move = moveMap[this.direction];
        if (move.x) head.x += move.x;
        if (move.y) head.y += move.y;

        this.snake.unshift(head);

        if (head.x === this.food.x && head.y === this.food.y) {
            this.updateScore();
            this.placeFood();
        } else {
            this.snake.pop();
        }
    }

    updateScore() {
        this.score += 1;
        document.getElementById('score').textContent = `Score: ${this.score}`;
    }

    checkCollision() {
        const head = this.snake[0];
        
        // Wall collision
        if (head.x < 0 || head.x >= this.canvas.width ||
            head.y < 0 || head.y >= this.canvas.height) {
            return true;
        }
        
        // Self collision
        return this.snake.slice(1).some(segment => 
            segment.x === head.x && segment.y === head.y
        );
    }

    draw() {
        this.drawBackground();
        this.drawGrid();
        this.drawSnake();
        this.drawFood();
    }

    drawBackground() {
        const bgGradient = this.ctx.createLinearGradient(0, 0, this.canvas.width, this.canvas.height);
        bgGradient.addColorStop(0, '#000000');
        bgGradient.addColorStop(1, '#1a1a1a');
        this.ctx.fillStyle = bgGradient;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }

    drawGrid() {
        this.ctx.strokeStyle = 'rgba(0, 255, 0, 0.1)';
        this.ctx.lineWidth = 0.5;
        
        for (let i = 0; i < this.canvas.width; i += this.BLOCK_SIZE) {
            this.ctx.beginPath();
            this.ctx.moveTo(i, 0);
            this.ctx.lineTo(i, this.canvas.height);
            this.ctx.stroke();
        }
        
        for (let i = 0; i < this.canvas.height; i += this.BLOCK_SIZE) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, i);
            this.ctx.lineTo(this.canvas.width, i);
            this.ctx.stroke();
        }
    }

    drawSnake() {
        this.snake.forEach((segment, index) => {
            this.ctx.shadowBlur = 10;
            this.ctx.shadowColor = '#00ff00';
            this.ctx.fillStyle = index === 0 ? '#00ff00' : this.snakeGradient;
            this.ctx.fillRect(segment.x, segment.y, this.BLOCK_SIZE - 2, this.BLOCK_SIZE - 2);
            this.ctx.shadowBlur = 0;
        });
    }

    drawFood() {
        this.ctx.shadowBlur = 15;
        this.ctx.shadowColor = '#ff0000';
        this.ctx.fillStyle = '#ff0000';
        this.ctx.beginPath();
        this.ctx.arc(
            this.food.x + this.BLOCK_SIZE/2, 
            this.food.y + this.BLOCK_SIZE/2, 
            this.BLOCK_SIZE/2 - 2, 
            0, 
            Math.PI * 2
        );
        this.ctx.fill();
        this.ctx.shadowBlur = 0;
    }

    async saveScore(retries = 3) {
        for (let i = 0; i < retries; i++) {
            try {
                const response = await fetch('/save_score', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        player_name: this.playerName,
                        score: this.score
                    })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error(`Attempt ${i + 1} failed:`, error);
                if (i === retries - 1) throw error;
                await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1))); // Exponential backoff
            }
        }
    }

    async gameOver() {
        this.gameRunning = false;
        document.getElementById('finalScore').textContent = this.score;
        document.getElementById('gameOver').style.display = 'block';

        try {
            await this.saveScore();
        } catch (error) {
            console.error('Error saving score:', error);
            // Show error message to user
            const gameOver = document.getElementById('gameOver');
            const errorMsg = document.createElement('p');
            errorMsg.style.color = 'red';
            errorMsg.textContent = 'Failed to save score. Please try again.';
            gameOver.insertBefore(errorMsg, gameOver.lastElementChild);
        }
    }

    cleanup() {
        // Remove event listeners to prevent memory leaks
        window.removeEventListener('resize', this.handleResize);
        document.removeEventListener('keydown', this.handleKeyPress);
        window.removeEventListener('beforeunload', this.cleanup);
        
        // Cancel any pending animation frame
        if (this.gameLoopTimeout) {
            clearTimeout(this.gameLoopTimeout);
        }
        
        // Clear game state
        this.gameRunning = false;
        this.snake = [];
        this.food = null;
    }

    restart() {
        this.score = 0;
        this.direction = 'RIGHT';
        document.getElementById('score').textContent = 'Score: 0';
        this.init();
    }

    gameLoop() {
        if (!this.gameRunning) return;
        
        this.moveSnake();
        
        if (this.checkCollision()) {
            this.gameOver();
            return;
        }
        
        this.draw();
        this.gameLoopTimeout = setTimeout(() => this.gameLoop(), 100);
    }

    pause() {
        if (this.gameRunning) {
            this.gameRunning = false;
            if (this.gameLoopTimeout) {
                clearTimeout(this.gameLoopTimeout);
            }
        }
    }

    resume() {
        if (!this.gameRunning) {
            this.gameRunning = true;
            this.gameLoop();
        }
    }
}

// Initialize game when document is loaded and add error handling
document.addEventListener('DOMContentLoaded', () => {
    try {
        window.game = new SnakeGame('gameCanvas');
    } catch (error) {
        console.error('Failed to initialize game:', error);
        document.body.innerHTML = '<div style="color: red; text-align: center; margin-top: 2em;">Failed to load game. Please refresh the page.</div>';
    }
});