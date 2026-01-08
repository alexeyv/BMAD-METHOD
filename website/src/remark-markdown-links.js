/**
 * Remark plugin to transform relative markdown links to absolute paths
 *
 * Uses the source file's path to resolve relative links correctly.
 * Works with Astro's build.format: 'directory' setting.
 */

import { visit } from 'unist-util-visit';
import path from 'path';

export default function remarkMarkdownLinks() {
  return (tree, file) => {
    const filePath = file.history?.[0] || file.path;

    // Debug log
    if (!remarkMarkdownLinks._logged) {
      console.log('[remark-markdown-links] Plugin running, file:', filePath || 'NO PATH');
      remarkMarkdownLinks._logged = true;
    }

    if (!filePath) return;

    // Extract docs-relative path
    const docsMatch = filePath.match(/(?:\/docs\/|\/content\/docs\/)(.+)$/);
    if (!docsMatch) return;

    const currentDir = path.dirname(docsMatch[1]);

    visit(tree, 'link', (node) => {
      const href = node.url;
      if (typeof href !== 'string') return;
      if (!href.startsWith('./') && !href.startsWith('../')) return;

      // Extract path and suffix
      const hashIdx = href.indexOf('#');
      const queryIdx = href.indexOf('?');
      const delimIdx = Math.min(hashIdx === -1 ? Infinity : hashIdx, queryIdx === -1 ? Infinity : queryIdx);

      const pathPortion = delimIdx === Infinity ? href : href.substring(0, delimIdx);
      const suffix = delimIdx === Infinity ? '' : href.substring(delimIdx);

      if (!pathPortion.endsWith('.md')) return;

      // Resolve relative path to absolute
      let resolved = path.posix.normalize(path.posix.join(currentDir, pathPortion));

      // Transform .md to directory path
      if (resolved.endsWith('/index.md')) {
        resolved = resolved.replace(/\/index\.md$/, '/');
      } else {
        resolved = resolved.replace(/\.md$/, '/');
      }

      if (!resolved.startsWith('/')) {
        resolved = '/' + resolved;
      }

      node.url = resolved + suffix;
    });
  };
}
