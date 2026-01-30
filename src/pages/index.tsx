import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          Survey of Software
        </Heading>
        <p className="hero__subtitle">Give your agents a map.</p>
      </div>
    </header>
  );
}

type NavCardProps = {
  title: string;
  description: string;
  link: string;
  icon: string;
};

function NavCard({title, description, link, icon}: NavCardProps) {
  return (
    <div className={clsx('col col--6 col--md-4 col--lg-2')}>
      <Link to={link} className="card" style={{
        height: '100%',
        padding: '1.5rem',
        textDecoration: 'none',
        border: '1px solid var(--ifm-color-emphasis-300)',
        borderRadius: '8px',
        display: 'flex',
        flexDirection: 'column',
        transition: 'transform 0.2s, border-color 0.2s',
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = 'translateY(-4px)';
        e.currentTarget.style.borderColor = 'var(--ifm-color-primary)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = 'translateY(0)';
        e.currentTarget.style.borderColor = 'var(--ifm-color-emphasis-300)';
      }}>
        <div style={{fontSize: '2.5rem', marginBottom: '1rem'}}>{icon}</div>
        <Heading as="h3" style={{marginBottom: '0.5rem'}}>{title}</Heading>
        <p style={{color: 'var(--ifm-color-emphasis-700)', margin: 0}}>{description}</p>
      </Link>
    </div>
  );
}

function NavigationCards() {
  const cards: NavCardProps[] = [
    {
      title: 'About',
      description: 'What this is and how to use it',
      link: '/about',
      icon: '📖',
    },
    {
      title: 'Collections',
      description: 'Thematic groupings for common use cases',
      link: '/collections',
      icon: '🎯',
    },
    {
      title: 'Vision',
      description: 'The origin story and long-term vision',
      link: '/vision',
      icon: '🗺️',
    },
    {
      title: 'Methodology',
      description: 'Replicate the research yourself',
      link: '/survey/replication',
      icon: '🔬',
    },
    {
      title: 'Survey',
      description: 'Browse the research library',
      link: '/survey',
      icon: '📚',
    },
  ];

  return (
    <section style={{padding: '4rem 0'}}>
      <div className="container">
        <div className="row" style={{gap: '2rem 0'}}>
          {cards.map((props, idx) => (
            <NavCard key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}


export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      description="Systematic library research for Python developers">
      <HomepageHeader />
      <main>
        <NavigationCards />
      </main>
    </Layout>
  );
}
