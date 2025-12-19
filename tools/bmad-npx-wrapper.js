#!/usr/bin/env node

/**
 * BMad Method CLI - Entry point for npx and local execution
 * Runs the interactive installer directly (no CLI framework needed)
 */

const chalk = require('chalk');
const { Installer } = require('./cli/installers/lib/core/installer');
const { UI } = require('./cli/lib/ui');

const packageJson = require('../package.json');

// Ignore legacy "install" subcommand for backwards compatibility
const args = new Set(process.argv.slice(2).filter((a) => a !== 'install'));

// Handle --version / -V
if (args.has('--version') || args.has('-V')) {
  console.log(packageJson.version);
  process.exit(0);
}

// Handle --help / -h
if (args.has('--help') || args.has('-h')) {
  console.log(`BMAD Method v${packageJson.version}`);
  console.log('\nUsage: npx bmad-method\n');
  console.log('Installs BMAD agents and workflows to your project.');
  console.log('Run from your project directory to start the interactive installer.\n');
  console.log('Options:');
  console.log('  --version, -V  Show version number');
  console.log('  --help, -h     Show this help message\n');
  process.exit(0);
}

// Validate no unknown arguments
const validArgs = new Set(['--version', '-V', '--help', '-h']);
const unknownArgs = [...args].filter((arg) => !validArgs.has(arg));
if (unknownArgs.length > 0) {
  console.error(chalk.red(`Unknown option: ${unknownArgs[0]}`));
  console.error(chalk.dim('Run with --help for usage information'));
  process.exit(1);
}

// Run installer directly
const ui = new UI();
const installer = new Installer();

(async () => {
  try {
    const config = await ui.promptInstall();

    // Handle cancel
    if (config.actionType === 'cancel') {
      console.log(chalk.yellow('Installation cancelled.'));
      process.exit(0);
    }

    // Handle quick update separately
    if (config.actionType === 'quick-update') {
      const result = await installer.quickUpdate(config);
      console.log(chalk.green('\n✨ Quick update complete!'));
      console.log(chalk.cyan(`Updated ${result.moduleCount} modules with preserved settings`));
      console.log(
        chalk.magenta(
          "\n📋 Want to see what's new? Check out the changelog: https://github.com/bmad-code-org/BMAD-METHOD/blob/main/CHANGELOG.md",
        ),
      );
      process.exit(0);
    }

    // Handle compile agents separately
    if (config.actionType === 'compile-agents') {
      const result = await installer.compileAgents(config);
      console.log(chalk.green('\n✨ Agent recompilation complete!'));
      console.log(chalk.cyan(`Recompiled ${result.agentCount} agents with customizations applied`));
      process.exit(0);
    }

    // Regular install/update flow
    const result = await installer.install(config);

    // Check if installation was cancelled
    if (result && result.cancelled) {
      process.exit(0);
    }

    // Check if installation succeeded
    if (result && result.success) {
      // Run AgentVibes installer if needed
      if (result.needsAgentVibes) {
        // Add some spacing before AgentVibes setup
        console.log('');
        console.log(chalk.magenta('🎙️  AgentVibes TTS Setup'));
        console.log(chalk.cyan('AgentVibes provides voice synthesis for BMAD agents with:'));
        console.log(chalk.dim('  • ElevenLabs AI (150+ premium voices)'));
        console.log(chalk.dim('  • Piper TTS (50+ free voices)\n'));

        const readline = require('node:readline');
        const rl = readline.createInterface({
          input: process.stdin,
          output: process.stdout,
        });

        await new Promise((resolve) => {
          rl.question(chalk.green('Press Enter to start AgentVibes installer...'), () => {
            rl.close();
            resolve();
          });
        });

        console.log('');

        // Run AgentVibes installer
        const { execSync } = require('node:child_process');
        try {
          execSync('npx agentvibes@latest install', {
            cwd: result.projectDir,
            stdio: 'inherit',
            shell: true,
          });
          console.log(chalk.green('\n✓ AgentVibes installation complete'));
          console.log(chalk.cyan('\n✨ BMAD with TTS is ready to use!'));
        } catch {
          console.log(chalk.yellow('\n⚠ AgentVibes installation was interrupted or failed'));
          console.log(chalk.cyan('You can run it manually later with:'));
          console.log(chalk.green(`  cd ${result.projectDir}`));
          console.log(chalk.green('  npx agentvibes install\n'));
        }
      }

      process.exit(0);
    }
  } catch (error) {
    // Check if error has a complete formatted message
    if (error.fullMessage) {
      console.error(error.fullMessage);
      if (error.stack) {
        console.error('\n' + chalk.dim(error.stack));
      }
    } else {
      // Generic error handling for all other errors
      console.error(chalk.red('Installation failed:'), error.message);
      console.error(chalk.dim(error.stack));
    }
    process.exit(1);
  }
})();
