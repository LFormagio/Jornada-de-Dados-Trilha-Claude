// src/utils/wordcloud.js
export function initWordCloud(canvasId, words) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let width = canvas.width;
  let height = canvas.height;
  const radius = Math.min(width, height) / 2 - 20;

  // Configuration
  const focalLength = 300;
  const baseSpeed = 0.005;
  let angleX = baseSpeed;
  let angleY = baseSpeed;
  
  // Mouse position relative to center
  let mouseX = 0;
  let mouseY = 0;
  let isMouseOver = false;

  canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left - width / 2;
    const y = e.clientY - rect.top - height / 2;
    
    // Convert mouse position to rotation speed
    mouseX = (y / (height/2)) * 0.02; // Vertical mouse controls X axis
    mouseY = (x / (width/2)) * 0.02;  // Horizontal mouse controls Y axis
    isMouseOver = true;
  });

  canvas.addEventListener('mouseleave', () => {
    isMouseOver = false;
  });

  class Tag {
    constructor(text, x, y, z) {
      this.text = text;
      this.x = x;
      this.y = y;
      this.z = z;
      
      // Determine importance (randomly emphasize some words)
      this.importance = Math.random();
      this.color = this.importance > 0.7 ? '#2563eb' : (this.importance > 0.3 ? '#e2e8f0' : '#94a3b8');
      this.baseFontSize = this.importance > 0.7 ? 22 : (this.importance > 0.3 ? 16 : 12);
    }

    draw() {
      // 3D to 2D projection
      const scale = focalLength / (focalLength + this.z);
      const x2d = this.x * scale + width / 2;
      const y2d = this.y * scale + height / 2;

      // Alpha based on depth
      const alpha = (this.z + radius) / (2 * radius);
      const alphaAdjusted = Math.max(0.1, 1 - alpha);

      ctx.save();
      ctx.globalAlpha = alphaAdjusted;
      ctx.translate(x2d, y2d);
      
      // Scale font based on depth projection
      const fontSize = this.baseFontSize * scale;
      ctx.font = `bold ${fontSize}px Inter, sans-serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      
      // Draw text
      ctx.fillStyle = this.color;
      ctx.fillText(this.text, 0, 0);
      
      ctx.restore();
    }
  }

  // Generate sphere points using Fibonacci spiral for even distribution
  const tags = [];
  const phi = Math.PI * (3 - Math.sqrt(5)); // golden angle
  
  for (let i = 0; i < words.length; i++) {
    const y = 1 - (i / (words.length - 1)) * 2; // y goes from 1 to -1
    const r = Math.sqrt(1 - y * y); // radius at y
    const theta = phi * i; // golden angle increment
    
    const x = Math.cos(theta) * r;
    const z = Math.sin(theta) * r;
    
    tags.push(new Tag(words[i], x * radius, y * radius, z * radius));
  }

  function rotateX(tag, angle) {
    const y = tag.y * Math.cos(angle) - tag.z * Math.sin(angle);
    const z = tag.y * Math.sin(angle) + tag.z * Math.cos(angle);
    tag.y = y;
    tag.z = z;
  }

  function rotateY(tag, angle) {
    const x = tag.x * Math.cos(angle) - tag.z * Math.sin(angle);
    const z = tag.x * Math.sin(angle) + tag.z * Math.cos(angle);
    tag.x = x;
    tag.z = z;
  }

  function animate() {
    ctx.clearRect(0, 0, width, height);

    // Smoothly transition to mouse speed or default speed
    const targetAngleX = isMouseOver ? mouseX : baseSpeed;
    const targetAngleY = isMouseOver ? mouseY : baseSpeed;
    
    angleX += (targetAngleX - angleX) * 0.1;
    angleY += (targetAngleY - angleY) * 0.1;

    // Sort by Z for proper rendering order (painter's algorithm)
    tags.sort((a, b) => b.z - a.z);

    for (const tag of tags) {
      rotateX(tag, angleX);
      rotateY(tag, angleY);
      tag.draw();
    }

    requestAnimationFrame(animate);
  }

  animate();
}
