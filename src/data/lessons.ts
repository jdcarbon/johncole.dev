export type LessonMeta = {
  slug: string;
  title: string;
  level: string;
  subject: string;
  duration: string;
  description: string;
  href: string;
};

export const lessons: LessonMeta[] = [
  {
    slug: 'functions-and-testing',
    title: 'Functions, Decomposition, and Testing',
    level: 'Introductory programming',
    subject: 'Python 3',
    duration: '60–75 minutes',
    description:
      'Turn a monolithic study-time tracker into small, testable functions—and learn why return values and tests make programs easier to change.',
    href: '/teaching/lessons/functions-and-testing/',
  },
  {
    slug: 'modeling-an-application',
    title: 'Modeling a Real-World Application',
    level: 'Intermediate / software engineering',
    subject: 'SQL and SQLite',
    duration: 'About 75 minutes',
    description:
      'Move from a vague subscription-tracking request to entities, relationships, constraints, and queries that match a deliberately limited scope.',
    href: '/teaching/lessons/modeling-an-application/',
  },
  {
    slug: 'evaluating-ai-code',
    title: 'Evaluating AI-Generated Code',
    level: 'Intermediate software engineering',
    subject: 'Python 3',
    duration: 'About 75 minutes',
    description:
      'Turn an underspecified CSV-import prompt into acceptance criteria, expose defects in a plausible generated implementation, and decide what tests do—and do not—establish.',
    href: '/teaching/lessons/evaluating-ai-code/',
  },
];

export function getLesson(slug: string): LessonMeta | undefined {
  return lessons.find((l) => l.slug === slug);
}

export function getAdjacentLessons(slug: string): {
  prev: LessonMeta | null;
  next: LessonMeta | null;
  index: number;
} {
  const index = lessons.findIndex((l) => l.slug === slug);
  return {
    index,
    prev: index > 0 ? lessons[index - 1] : null,
    next: index >= 0 && index < lessons.length - 1 ? lessons[index + 1] : null,
  };
}
