'use strict';
const stage = document.querySelector('.figure-stage');
const media = stage.querySelector('svg, img');
const status = document.getElementById('zoom-status');
document.querySelectorAll('[data-scale]').forEach(button => {
  button.addEventListener('click', () => {
    const scale = button.dataset.scale;
    media.style.width = scale === 'fit' ? '100%' : `${Number(stage.dataset.width) * Number(scale)}px`;
    media.style.maxWidth = scale === 'fit' ? '100%' : 'none';
    stage.scrollTo(0, 0);
    document.querySelectorAll('[data-scale]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    status.textContent = button.textContent;
  });
});
