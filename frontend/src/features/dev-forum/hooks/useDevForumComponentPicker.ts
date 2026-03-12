import { useEffect, useRef, useState } from 'react';

import type { SelectedComponentDescriptor } from '../types';

function buildSelector(element: HTMLElement): string {
  if (element.id) return `#${CSS.escape(element.id)}`;
  const chain: string[] = [];
  let current: HTMLElement | null = element;
  let depth = 0;
  while (current && current.tagName.toLowerCase() !== 'body' && depth < 6) {
    const tag = current.tagName.toLowerCase();
    const parentElement: HTMLElement | null = current.parentElement;
    if (!parentElement) break;
    const siblings = Array.from(parentElement.children).filter((entry): entry is Element => (
      entry instanceof Element && entry.tagName === current!.tagName
    ));
    const index = siblings.indexOf(current) + 1;
    chain.unshift(`${tag}:nth-of-type(${Math.max(index, 1)})`);
    current = parentElement;
    depth += 1;
  }
  return chain.length > 0 ? chain.join(' > ') : element.tagName.toLowerCase();
}

function makeSelectedComponentDescriptor(element: HTMLElement): SelectedComponentDescriptor {
  return {
    selector: buildSelector(element),
    tag: element.tagName.toLowerCase(),
    id: element.id || '',
    class_name: element.className || '',
    text_sample: (element.textContent || '').trim().slice(0, 120),
  };
}

export function useDevForumComponentPicker() {
  const [pickingComponent, setPickingComponent] = useState(false);
  const [selectedComponent, setSelectedComponent] = useState<SelectedComponentDescriptor | null>(null);
  const hoveredElementRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!pickingComponent) return;

    const clearLiveHighlight = () => {
      if (hoveredElementRef.current) {
        hoveredElementRef.current.classList.remove('dev-forum-live-highlight');
        hoveredElementRef.current = null;
      }
    };

    const updateHovered = (target: Element | null) => {
      const next = target instanceof HTMLElement ? target : null;
      if (hoveredElementRef.current === next) return;
      if (hoveredElementRef.current) {
        hoveredElementRef.current.classList.remove('dev-forum-live-highlight');
      }
      hoveredElementRef.current = next;
      if (hoveredElementRef.current) {
        hoveredElementRef.current.classList.add('dev-forum-live-highlight');
      }
    };

    const onMouseMove = (event: MouseEvent) => {
      const target = document.elementFromPoint(event.clientX, event.clientY);
      updateHovered(target);
    };

    const stopAndCleanup = () => {
      setPickingComponent(false);
      clearLiveHighlight();
    };

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Enter') {
        event.preventDefault();
        event.stopPropagation();
        const target = hoveredElementRef.current;
        if (target) {
          setSelectedComponent(makeSelectedComponentDescriptor(target));
        }
        stopAndCleanup();
        return;
      }
      if (event.key === 'Escape') {
        event.preventDefault();
        event.stopPropagation();
        stopAndCleanup();
      }
    };

    const onClick = (event: MouseEvent) => {
      event.preventDefault();
      event.stopPropagation();
    };

    document.addEventListener('mousemove', onMouseMove, true);
    document.addEventListener('keydown', onKeyDown, true);
    document.addEventListener('click', onClick, true);

    return () => {
      document.removeEventListener('mousemove', onMouseMove, true);
      document.removeEventListener('keydown', onKeyDown, true);
      document.removeEventListener('click', onClick, true);
      clearLiveHighlight();
    };
  }, [pickingComponent]);

  return {
    pickingComponent,
    selectedComponent,
    startPicking: () => setPickingComponent(true),
    stopPicking: () => setPickingComponent(false),
    clearSelectedComponent: () => setSelectedComponent(null),
  };
}
