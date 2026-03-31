import { useEffect, useRef, useState } from 'react';
import './RichTextEditor.css';

interface RichTextEditorProps {
  value: string;
  onChange: (next: string) => void;
  ariaLabel?: string;
  boldTitle?: string;
  italicTitle?: string;
  underlineTitle?: string;
  minHeightRem?: number;
}

type FormatCommand = 'bold' | 'italic' | 'underline';

export default function RichTextEditor({
  value,
  onChange,
  ariaLabel = 'Rich text editor',
  boldTitle = 'Bold',
  italicTitle = 'Italic',
  underlineTitle = 'Underline',
  minHeightRem = 5.2,
}: RichTextEditorProps) {
  const editorRef = useRef<HTMLDivElement | null>(null);
  const [active, setActive] = useState<Record<FormatCommand, boolean>>({
    bold: false,
    italic: false,
    underline: false,
  });

  useEffect(() => {
    const editor = editorRef.current;
    if (!editor) return;
    if (editor.innerHTML !== value) {
      editor.innerHTML = value;
    }
  }, [value]);

  useEffect(() => {
    const onSelectionChange = () => {
      if (!editorRef.current) return;
      const selection = document.getSelection();
      if (!selection || selection.rangeCount === 0) return;
      const anchorNode = selection.anchorNode;
      if (!anchorNode) return;
      if (!editorRef.current.contains(anchorNode)) return;
      setActive({
        bold: document.queryCommandState('bold'),
        italic: document.queryCommandState('italic'),
        underline: document.queryCommandState('underline'),
      });
    };
    document.addEventListener('selectionchange', onSelectionChange);
    return () => document.removeEventListener('selectionchange', onSelectionChange);
  }, []);

  const apply = (command: FormatCommand) => {
    editorRef.current?.focus();
    document.execCommand(command);
    onChange(editorRef.current?.innerHTML ?? '');
    setActive((prev) => ({ ...prev, [command]: !prev[command] }));
  };

  return (
    <div className="rte">
      <div className="rte-toolbar" role="toolbar" aria-label={ariaLabel}>
        <button type="button" className={`rte-btn ${active.bold ? 'active' : ''}`} onClick={() => apply('bold')} title={boldTitle} aria-label={boldTitle}>
          <strong>B</strong>
        </button>
        <button type="button" className={`rte-btn ${active.italic ? 'active' : ''}`} onClick={() => apply('italic')} title={italicTitle} aria-label={italicTitle}>
          <em>I</em>
        </button>
        <button type="button" className={`rte-btn ${active.underline ? 'active' : ''}`} onClick={() => apply('underline')} title={underlineTitle} aria-label={underlineTitle}>
          <u>U</u>
        </button>
      </div>
      <div
        ref={editorRef}
        className="rte-area"
        contentEditable
        dir="ltr"
        suppressContentEditableWarning
        style={{ minHeight: `${minHeightRem}rem` }}
        onInput={(event) => onChange((event.currentTarget as HTMLDivElement).innerHTML)}
      />
    </div>
  );
}

