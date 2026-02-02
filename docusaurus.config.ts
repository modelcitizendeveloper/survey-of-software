import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Survey of Software | Model Citizen Developer',
  tagline: 'Mapping the Territory for Model Citizen Developers',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://research.modelcitizendeveloper.com',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'modelcitizendeveloper', // GitHub org/user name.
  projectName: 'survey-of-software', // Repo name.

  onBrokenLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/', // Make docs the root path
          sidebarPath: './sidebars.ts',
          editUrl:
            'https://github.com/modelcitizendeveloper/survey-of-software/tree/main/',
        },
        blog: false, // Disable blog
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Model Citizen Developer',
      logo: {
        alt: 'MCD Research Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'surveySidebar',
          position: 'left',
          label: 'The Survey',
        },
        {
          href: 'https://newsletter.modelcitizendeveloper.com/newsletter',
          label: 'Newsletter',
          position: 'right',
        },
        {
          href: 'https://github.com/modelcitizendeveloper/survey-of-software',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Research',
          items: [
            {
              label: 'About',
              to: '/about',
            },
            {
              label: 'Vision',
              to: '/vision',
            },
            {
              label: 'Replication',
              to: '/survey/replication',
            },
            {
              label: 'The Survey',
              to: '/survey',
            },
          ],
        },
        {
          title: 'Model Citizen Developer',
          items: [
            {
              label: 'Newsletter',
              href: 'https://newsletter.modelcitizendeveloper.com/newsletter',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/modelcitizendeveloper/survey-of-software',
            },
          ],
        },
      ],
      copyright: `© ${new Date().getFullYear()} Model Citizen Developer. Licensed under <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener noreferrer">CC BY 4.0</a>. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
