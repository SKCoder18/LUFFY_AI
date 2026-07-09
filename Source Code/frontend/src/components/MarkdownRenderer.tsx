import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Check, Copy } from 'lucide-react';

interface MarkdownRendererProps {
  content: string;
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        code(props) {
          const { children, className, node, ref, ...rest } = props;
          const match = /language-(\w+)/.exec(className || '');
          const isInline = !match && !className;
          
          if (isInline) {
            return (
              <code className="bg-gray-800 text-gray-200 px-1 py-0.5 rounded text-sm" {...rest}>
                {children}
              </code>
            );
          }
          
          const language = match ? match[1] : 'text';
          const codeString = String(children).replace(/\n$/, '');

          return (
            <div className="relative group my-4 rounded-md overflow-hidden bg-[#1e1e1e] border border-gray-700/50">
              <div className="flex items-center justify-between px-4 py-2 bg-gray-800/80 border-b border-gray-700/50">
                <span className="text-xs text-gray-400 font-mono">{language}</span>
                <CopyButton text={codeString} />
              </div>
              <SyntaxHighlighter
                {...rest}
                PreTag="div"
                children={codeString}
                language={language}
                style={vscDarkPlus}
                customStyle={{
                  margin: 0,
                  padding: '1rem',
                  background: 'transparent',
                  fontSize: '0.875rem'
                }}
              />
            </div>
          );
        },
        table(props) {
          return (
            <div className="overflow-x-auto my-4 rounded-md border border-gray-700/50">
              <table className="w-full text-sm text-left text-gray-300" {...props} />
            </div>
          );
        },
        thead(props) {
          return <thead className="text-xs text-gray-400 uppercase bg-gray-800/50" {...props} />;
        },
        th(props) {
          return <th className="px-4 py-3" {...props} />;
        },
        td(props) {
          return <td className="px-4 py-3 border-t border-gray-700/50" {...props} />;
        },
        a(props) {
          return <a className="text-blue-400 hover:underline" target="_blank" rel="noopener noreferrer" {...props} />;
        }
      }}
    >
      {content}
    </ReactMarkdown>
  );
};

const CopyButton = ({ text }: { text: string }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text', err);
    }
  };

  return (
    <button
      onClick={handleCopy}
      className="p-1 hover:bg-gray-700 rounded transition-colors text-gray-400 hover:text-gray-200 focus:outline-none"
      title="Copy code"
    >
      {copied ? <Check size={14} className="text-green-400" /> : <Copy size={14} />}
    </button>
  );
};
