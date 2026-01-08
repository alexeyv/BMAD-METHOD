/**
 * Remark plugin to transform markdown links for proper deployment
 *
 * - Resolves relative links (./ and ../) using the source file's path
 * - Prepends base path to absolute links (/) for subdirectory deployments
 * - Works with Astro's build.format: 'directory' setting
 */

import { visit } from 'unist-util-visit';
import path from 'path';

// Get base path from environment, strip trailing slash for concatenation
const basePath = (process.env.BASE_PATH || '').replace(/\/$/, '');

export default function remarkMarkdownLinks() {
  return (tree, file) => {
    const filePath = file.history?.[0] || file.path;

    // Debug log
    if (!remarkMarkdownLinks._logged) {
      console.log('[remark-markdown-links] Plugin running, basePath:', basePath || '(none)');
      remarkMarkdownLinks._logged = true;
    }

    // Extract docs-relative path for resolving relative links
    const docsMatch = filePath?.match(/(?:\/docs\/|\/content\/docs\/)(.+)$/);
    const currentDir = docsMatch ? path.dirname(docsMatch[1]) : null;

    visit(tree, 'link', (node) => {
      const href = node.url;
      if (typeof href !== 'string') return;

      // Skip external links and special protocols
      if (
        href.startsWith('http://') ||
        href.startsWith('https://') ||
        href.startsWith('mailto:') ||
        href.startsWith('tel:') ||
        href.startsWith('#')
      )
        return;

      // Extract path and suffix (hash/query)
      const hashIdx = href.indexOf('#');
      const queryIdx = href.indexOf('?');
      const delimIdx = Math.min(hashIdx === -1 ? Infinity : hashIdx, queryIdx === -1 ? Infinity : queryIdx);
      const pathPortion = delimIdx === Infinity ? href : href.substring(0, delimIdx);
      const suffix = delimIdx === Infinity ? '' : href.substring(delimIdx);

      // Handle absolute paths - just prepend base path
      if (href.startsWith('/')) {
        node.url = basePath + href;
        return;
      }

      // Handle relative paths - need to resolve against current file location
      if (!currentDir) return;
      if (!href.startsWith('./') && !href.startsWith('../')) return;

      // Resolve relative path to absolute
      let resolved = path.posix.normalize(path.posix.join(currentDir, pathPortion));

      // Transform .md links to directory paths
      if (pathPortion.endsWith('.md')) {
        if (resolved.endsWith('/index.md')) {
          resolved = resolved.replace(/\/index\.md$/, '/');
        } else {
          resolved = resolved.replace(/\.md$/, '/');
        }
      }

      if (!resolved.startsWith('/')) {
        resolved = '/' + resolved;
      }

      // Prepend base path for deployment
      node.url = basePath + resolved + suffix;
    });
  };
}
