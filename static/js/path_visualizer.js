/**
 * Path Optimization Visualizer
 * Creates industry-grade visualizations of cutting paths
 */

class PathVisualizer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        
        this.ctx = this.canvas.getContext('2d');
        this.entities = [];
        this.optimizedPath = [];
        this.originalPath = [];
        this.scale = 1;
        this.offsetX = 0;
        this.offsetY = 0;
        
        this.setupCanvas();
    }
    
    setupCanvas() {
        // Set canvas size
        const container = this.canvas.parentElement;
        this.canvas.width = container.clientWidth;
        this.canvas.height = 400;
        
        // High DPI support
        const dpr = window.devicePixelRatio || 1;
        const rect = this.canvas.getBoundingClientRect();
        this.canvas.width = rect.width * dpr;
        this.canvas.height = rect.height * dpr;
        this.ctx.scale(dpr, dpr);
        this.canvas.style.width = rect.width + 'px';
        this.canvas.style.height = rect.height + 'px';
    }
    
    loadGeometry(geometryData) {
        if (!geometryData || !geometryData.entities) return;
        
        this.entities = geometryData.entities.filter(e => 
            ['LINE', 'ARC', 'CIRCLE', 'LWPOLYLINE', 'POLYLINE'].includes(e.type)
        );
        
        // Extract points for visualization
        this.originalPath = this.extractPathPoints(this.entities);
        this.optimizedPath = this.optimizePath(this.originalPath);
        
        this.calculateBounds();
        this.draw();
    }
    
    extractPathPoints(entities) {
        const points = [];
        
        entities.forEach(entity => {
            if (entity.type === 'LINE' && entity.start && entity.end) {
                points.push({
                    x: entity.start[0] || entity.start.x,
                    y: entity.start[1] || entity.start.y,
                    type: 'start'
                });
                points.push({
                    x: entity.end[0] || entity.end.x,
                    y: entity.end[1] || entity.end.y,
                    type: 'end',
                    entity: entity
                });
            } else if (entity.type === 'CIRCLE' && entity.center) {
                const center = entity.center;
                points.push({
                    x: center[0] || center.x,
                    y: center[1] || center.y,
                    type: 'circle',
                    radius: entity.radius,
                    entity: entity
                });
            } else if (entity.type === 'ARC' && entity.center) {
                const center = entity.center;
                points.push({
                    x: center[0] || center.x,
                    y: center[1] || center.y,
                    type: 'arc',
                    radius: entity.radius,
                    entity: entity
                });
            } else if (entity.points && Array.isArray(entity.points)) {
                entity.points.forEach((point, idx) => {
                    if (Array.isArray(point) && point.length >= 2) {
                        points.push({
                            x: point[0],
                            y: point[1],
                            type: 'polyline',
                            index: idx,
                            entity: entity
                        });
                    }
                });
            }
        });
        
        return points;
    }
    
    optimizePath(points) {
        if (points.length < 2) return points;
        
        // Nearest Neighbor Algorithm (TSP-like)
        const optimized = [];
        const remaining = [...points];
        
        // Start with first point
        let current = remaining.shift();
        optimized.push(current);
        
        while (remaining.length > 0) {
            let nearestIdx = 0;
            let minDist = Infinity;
            
            // Find nearest unvisited point
            for (let i = 0; i < remaining.length; i++) {
                const dist = this.distance(current, remaining[i]);
                if (dist < minDist) {
                    minDist = dist;
                    nearestIdx = i;
                }
            }
            
            current = remaining.splice(nearestIdx, 1)[0];
            optimized.push(current);
        }
        
        return optimized;
    }
    
    distance(p1, p2) {
        const dx = p1.x - p2.x;
        const dy = p1.y - p2.y;
        return Math.sqrt(dx * dx + dy * dy);
    }
    
    calculateBounds() {
        if (this.originalPath.length === 0) return;
        
        let minX = Infinity, minY = Infinity;
        let maxX = -Infinity, maxY = -Infinity;
        
        this.originalPath.forEach(p => {
            minX = Math.min(minX, p.x);
            minY = Math.min(minY, p.y);
            maxX = Math.max(maxX, p.x);
            maxY = Math.max(maxY, p.y);
        });
        
        const width = maxX - minX;
        const height = maxY - minY;
        const padding = 50;
        
        const canvasWidth = this.canvas.width / (window.devicePixelRatio || 1);
        const canvasHeight = this.canvas.height / (window.devicePixelRatio || 1);
        
        this.scale = Math.min(
            (canvasWidth - padding * 2) / width,
            (canvasHeight - padding * 2) / height
        ) || 1;
        
        this.offsetX = (canvasWidth - width * this.scale) / 2 - minX * this.scale;
        this.offsetY = (canvasHeight - height * this.scale) / 2 - minY * this.scale;
    }
    
    transformX(x) {
        return x * this.scale + this.offsetX;
    }
    
    transformY(y) {
        return y * this.scale + this.offsetY;
    }
    
    draw() {
        const ctx = this.ctx;
        const dpr = window.devicePixelRatio || 1;
        const width = this.canvas.width / dpr;
        const height = this.canvas.height / dpr;
        
        // Clear canvas
        ctx.clearRect(0, 0, width, height);
        
        // Draw grid background
        this.drawGrid(ctx, width, height);
        
        // Draw original path (gray)
        this.drawPath(ctx, this.originalPath, '#94a3b8', 1, false);
        
        // Draw optimized path (green)
        this.drawPath(ctx, this.optimizedPath, '#16a34a', 2, true);
        
        // Draw statistics
        this.drawStats(ctx, width, height);
    }
    
    drawGrid(ctx, width, height) {
        ctx.strokeStyle = '#e2e8f0';
        ctx.lineWidth = 0.5;
        
        const gridSize = 20;
        for (let x = 0; x < width; x += gridSize) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, height);
            ctx.stroke();
        }
        for (let y = 0; y < height; y += gridSize) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }
    }
    
    drawPath(ctx, path, color, lineWidth, showArrows) {
        if (path.length < 2) return;
        
        ctx.strokeStyle = color;
        ctx.lineWidth = lineWidth;
        ctx.setLineDash([]);
        
        // Draw path lines
        ctx.beginPath();
        for (let i = 0; i < path.length - 1; i++) {
            const p1 = path[i];
            const p2 = path[i + 1];
            
            const x1 = this.transformX(p1.x);
            const y1 = this.transformY(p1.y);
            const x2 = this.transformX(p2.x);
            const y2 = this.transformY(p2.y);
            
            if (i === 0) {
                ctx.moveTo(x1, y1);
            }
            ctx.lineTo(x2, y2);
            
            // Draw arrow for optimized path
            if (showArrows && i % 3 === 0) {
                this.drawArrow(ctx, x1, y1, x2, y2, color);
            }
        }
        ctx.stroke();
        
        // Draw points
        path.forEach((p, i) => {
            const x = this.transformX(p.x);
            const y = this.transformY(p.y);
            
            ctx.fillStyle = i === 0 ? '#ef4444' : (i === path.length - 1 ? '#3b82f6' : color);
            ctx.beginPath();
            ctx.arc(x, y, i === 0 || i === path.length - 1 ? 4 : 2, 0, Math.PI * 2);
            ctx.fill();
            
            // Start/End labels
            if (i === 0) {
                ctx.fillStyle = '#ef4444';
                ctx.font = '10px Arial';
                ctx.fillText('START', x + 8, y - 8);
            } else if (i === path.length - 1) {
                ctx.fillStyle = '#3b82f6';
                ctx.font = '10px Arial';
                ctx.fillText('END', x + 8, y - 8);
            }
        });
    }
    
    drawArrow(ctx, x1, y1, x2, y2, color) {
        const angle = Math.atan2(y2 - y1, x2 - x1);
        const arrowLength = 8;
        const arrowWidth = 4;
        
        ctx.save();
        ctx.translate(x2, y2);
        ctx.rotate(angle);
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(-arrowLength, -arrowWidth);
        ctx.lineTo(-arrowLength, arrowWidth);
        ctx.closePath();
        ctx.fill();
        ctx.restore();
    }
    
    drawStats(ctx, width, height) {
        const originalDist = this.calculateTotalDistance(this.originalPath);
        const optimizedDist = this.calculateTotalDistance(this.optimizedPath);
        const savings = originalDist > 0 ? ((originalDist - optimizedDist) / originalDist * 100) : 0;
        
        // Draw info box
        ctx.fillStyle = 'rgba(255, 255, 255, 0.95)';
        ctx.strokeStyle = '#e2e8f0';
        ctx.lineWidth = 1;
        ctx.fillRect(10, 10, 200, 100);
        ctx.strokeRect(10, 10, 200, 100);
        
        ctx.fillStyle = '#0f172a';
        ctx.font = 'bold 12px Arial';
        ctx.fillText('Path Optimization', 20, 28);
        
        ctx.font = '10px Arial';
        ctx.fillStyle = '#64748b';
        ctx.fillText(`Original Distance: ${originalDist.toFixed(1)} mm`, 20, 48);
        ctx.fillText(`Optimized Distance: ${optimizedDist.toFixed(1)} mm`, 20, 63);
        ctx.fillStyle = savings > 0 ? '#16a34a' : '#64748b';
        ctx.fillText(`Savings: ${savings.toFixed(1)}%`, 20, 78);
        
        // Legend
        ctx.fillStyle = '#94a3b8';
        ctx.fillRect(20, height - 60, 12, 2);
        ctx.fillText('Original Path', 35, height - 55);
        
        ctx.fillStyle = '#16a34a';
        ctx.fillRect(20, height - 40, 12, 2);
        ctx.fillText('Optimized Path', 35, height - 35);
        
        ctx.fillStyle = '#ef4444';
        ctx.beginPath();
        ctx.arc(26, height - 20, 3, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#0f172a';
        ctx.fillText('Start', 35, height - 17);
        
        ctx.fillStyle = '#3b82f6';
        ctx.beginPath();
        ctx.arc(76, height - 20, 3, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#0f172a';
        ctx.fillText('End', 85, height - 17);
    }
    
    calculateTotalDistance(path) {
        let total = 0;
        for (let i = 0; i < path.length - 1; i++) {
            total += this.distance(path[i], path[i + 1]);
        }
        return total;
    }
}

// Export for use in HTML
if (typeof window !== 'undefined') {
    window.PathVisualizer = PathVisualizer;
}

