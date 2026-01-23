import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Breadth',
    description: (
      <>
        Systematic coverage across algorithm libraries, data processing tools, ML frameworks, and modern development stacks.
        Quick landscape scans reveal what exists in each category.
      </>
    ),
  },
  {
    title: 'Depth',
    description: (
      <>
        Performance benchmarks, feature matrices, trade-off analysis.
        Deep technical dives when you need implementation details.
      </>
    ),
  },
  {
    title: 'Open & Replicable',
    description: (
      <>
        All research published on GitHub. Methodology and sources documented.
        You can verify it, replicate it, and build on it.
      </>
    ),
  },
];

function Feature({title, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
