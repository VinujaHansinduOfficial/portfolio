import React, { useState, useEffect, useRef, useMemo, useCallback } from "react";
import {
  Menu,
  X,
  Download,
  Globe,
  Mail,
  Phone,
  MapPin,
  Code2,
  Smartphone,
  Database,
  ChevronLeft,
  ChevronRight,
  CheckCircle2,
  ArrowLeft,
  Send,
} from "lucide-react";

/* Brand icons as inline SVG — lucide-react removed Github/Linkedin. */
function GithubIcon({ size = 20, className = "" }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="currentColor"
      aria-hidden="true"
      className={className}
    >
      <path d="M12 .5A11.5 11.5 0 0 0 .5 12a11.5 11.5 0 0 0 7.86 10.92c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.37-3.88-1.37-.53-1.34-1.29-1.7-1.29-1.7-1.05-.72.08-.7.08-.7 1.16.08 1.77 1.2 1.77 1.2 1.03 1.77 2.7 1.26 3.36.97.1-.75.4-1.26.73-1.55-2.56-.29-5.25-1.28-5.25-5.7 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.46.11-3.04 0 0 .97-.31 3.18 1.18a11 11 0 0 1 5.8 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.58.23 2.75.12 3.04.74.81 1.18 1.84 1.18 3.1 0 4.43-2.69 5.4-5.26 5.69.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 23.5 12 11.5 11.5 0 0 0 12 .5Z" />
    </svg>
  );
}

function LinkedinIcon({ size = 20, className = "" }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="currentColor"
      aria-hidden="true"
      className={className}
    >
      <path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9h4v12H3V9Zm7 0h3.8v1.64h.06A4.17 4.17 0 0 1 17.6 8.7c4 0 4.75 2.5 4.75 5.76V21h-4v-5.75c0-1.37-.03-3.14-1.96-3.14-1.96 0-2.26 1.5-2.26 3.05V21h-4V9Z" />
    </svg>
  );
}

/* ------------------------------------------------------------------
   1. YOUR CONTENT — edit everything in this block, nothing else.
------------------------------------------------------------------ */

const PROFILE = {
  name: "Vinuja Hansindu",
  handle: "vinujahansindu",
  roles: [
    "Software Engineering Undergraduate",
    "Mobile App Developer",
    "Full-Stack Developer",
  ],
  intro:
    "A motivated Software Engineering undergraduate with a strong desire to become an expert in the field. I learn quickly, coordinate and organise well, and work proactively in complex environments to deliver high-quality software.",
  email: "vinujahansinduofficial@gmail.com",
  phone: "+94 71 418 6644",
  address: "465A, Galle Road, Ambalangoda (80300)",
  mapQuery: "Ambalangoda, Sri Lanka",
  github: "https://github.com/yourname",
  linkedin: "https://linkedin.com/in/yourname",
  cvUrl: "/cv.pdf",
  // Put profile.jpg in your project's /public folder.
  photo: "/profile.jpg",
};

// The contact form posts here. FormSubmit needs one confirmation click:
// the first message you send triggers an activation email to the address below.
const FORM_ENDPOINT = `https://formsubmit.co/ajax/${PROFILE.email}`;

const EDUCATION = [
  {
    label: "Degree",
    value: "Bachelor of Information Technology (Undergraduate), SLIIT — 2022–2026",
  },
  { label: "A/L", value: "G/ Dharmasoka College, Ambalangoda — 2020" },
  { label: "O/L", value: "G/ Dharmasoka College, Ambalangoda — 2017" },
];

const EXPERIENCE = [
  {
    role: "Software Engineering Intern",
    org: "SLT Mobitel Head Office",
    period: "Jan 2025 – Jul 2025",
  },
];

// Ring percentages are your call — tweak each `level` to how you rate yourself.
const SKILLS = [
  { name: "Java", level: 85 },
  { name: "React.js", level: 85 },
  { name: "Flutter", level: 80 },
  { name: "Spring Boot", level: 75 },
  { name: "Python", level: 75 },
  { name: "MySQL", level: 85 },
  { name: "Next.js", level: 70 },
  { name: "Kotlin", level: 70 },
];

const TOOLBOX = [
  { group: "Programming", items: ["Java", "Python", "C", "C++"] },
  { group: "Web", items: ["HTML5", "CSS3", "PHP", "JavaScript"] },
  { group: "Mobile", items: ["Flutter", "Dart", "Kotlin"] },
  { group: "Frameworks", items: ["React.js", "Next.js", "Spring Boot", "FastAPI"] },
  { group: "Databases", items: ["MySQL", "MS SQL Server", "Oracle", "MongoDB"] },
  { group: "Tools", items: ["REST APIs", "Figma", "Photoshop"] },
];

const LANGUAGES = ["English", "Sinhala"];

const SERVICES = [
  {
    icon: Code2,
    title: "Web Development",
    body: "Full-stack web apps with React.js, Next.js and Spring Boot.",
  },
  {
    icon: Smartphone,
    title: "Mobile Apps",
    body: "Android and cross-platform apps built with Flutter and Kotlin.",
  },
  {
    icon: Database,
    title: "Databases & APIs",
    body: "Relational and NoSQL schema design backed by clean REST APIs.",
  },
];

const PROJECTS = [
  {
    id: "mental-health-ai",
    title: "AI Mobile App for Early Identification of Student Mental Health",
    cardTitle: "Student Wellbeing AI Platform",
    kind: "Final year research project · Group · 2026",
    tagline:
      "Multimodal AI platform that flags student wellbeing risks early, with a Flutter app and a web dashboard.",
    tech: [
      "Flutter",
      "FastAPI",
      "MongoDB",
      "Python",
      "Machine Learning",
      "Deep Learning",
      "NLP",
      "LSTM",
      "ARIMA",
      "CNN",
    ],
    about: [
      "A multimodal AI platform for the early identification, monitoring and prediction of student mental-health risk, built as my final year research project.",
      "It analyses behavioural, psychological, academic, physiological, textual and facial-emotion data, combining risk classification, NLP journal analysis, facial emotion recognition and time-series forecasting. Students use a Flutter mobile app; counsellors work from a web dashboard.",
    ],
    features: [
      "Risk classification with Random Forest and logistic regression",
      "NLP analysis of student journal entries",
      "Facial emotion recognition using a CNN",
      "Time-series forecasting with LSTM and ARIMA",
      "Flutter mobile app for students",
      "Professional web dashboard for counsellors",
    ],
    live: "",
    repo: "https://github.com/yourname/student-wellbeing-ai",
    shots: ["App home", "Journal analysis", "Risk dashboard", "Forecast view"],
    hue: 265,
  },
  {
    id: "frd",
    title: "FRD Security Attendance Management System — SLT",
    cardTitle: "FRD Security Attendance System",
    kind: "Group project · 2025",
    tagline:
      "Attendance management for security officers at SLT Mobitel, with a two-step approval flow.",
    tech: ["React.js", "Spring Boot", "MySQL", "Microsoft Azure Active Directory"],
    about: [
      "FRD Security Attendance Management System is the attendance management system for security officers at SLT Mobitel.",
      "It covers CRUD operations, user level management, daily attendance entry, attendance report generation and a two-step approval system.",
    ],
    features: [
      "Azure Active Directory authentication and authorization",
      "Role based user dashboards",
      "Daily attendance marking and scheduled shifts",
      "Two step approval system with approval history",
      "Daily and monthly attendance reports",
      "Fully responsive design",
    ],
    live: "",
    repo: "https://github.com/yourname/frd-attendance",
    shots: ["Login screen", "Manager dashboard", "Approval history", "Monthly report"],
    hue: 210,
  },
  {
    id: "skillsync",
    title: "SkillSync Freelance Marketplace Platform",
    cardTitle: "SkillSync Freelance Marketplace",
    kind: "Group project · 2025",
    tagline:
      "Web platform connecting international clients with skilled freelancers from Sri Lanka.",
    tech: ["Spring Boot", "React.js", "MySQL"],
    about: [
      "SkillSync is a web application that connects international clients with skilled freelancers from Sri Lanka.",
      "Clients post job ads while freelancers showcase their profiles and services, which streamlines finding and managing freelance work on both sides.",
    ],
    features: [
      "Separate client and freelancer accounts",
      "Job ad posting and browsing",
      "Freelancer profiles with services and portfolios",
      "Proposal and hiring workflow",
      "Search and filtering by skill",
      "Fully responsive design",
    ],
    live: "",
    repo: "https://github.com/yourname/skillsync",
    shots: ["Landing page", "Job listings", "Freelancer profile", "Client dashboard"],
    hue: 175,
  },
  {
    id: "numenor",
    title: "Legend of the Numenor — 2D Mobile Game",
    cardTitle: "Legend of the Numenor",
    kind: "Individual project · 2024",
    tagline: "A 2D Android adventure game with joystick controls, built in Kotlin.",
    tech: ["Kotlin", "XML", "Android"],
    about: [
      "A 2D mobile game inspired by high-fantasy adventure, built as an individual project.",
      "The game keeps its controls deliberately simple: an on-screen graphical joystick drives the character through each level, which keeps the experience engaging without a tutorial.",
    ],
    features: [
      "On-screen graphical joystick controls",
      "Sprite based 2D character animation",
      "Level progression with obstacles",
      "Score tracking",
      "Built natively for Android in Kotlin",
      "Lightweight, runs on low-end devices",
    ],
    live: "",
    repo: "https://github.com/yourname/legend-of-the-numenor",
    shots: ["Title screen", "Gameplay", "Level select", "Score screen"],
    hue: 30,
  },
];

const NAV = [
  { id: "home", label: "Home" },
  { id: "about", label: "About" },
  { id: "services", label: "Services" },
  { id: "projects", label: "Projects" },
  { id: "contact", label: "Contact" },
];

/* ------------------------------------------------------------------
   2. Small hooks
------------------------------------------------------------------ */

function useTypewriter(words, typeSpeed = 95, deleteSpeed = 45, pause = 1500) {
  const [index, setIndex] = useState(0);
  const [text, setText] = useState("");
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const word = words[index % words.length];
    let timer;
    if (!deleting && text === word) {
      timer = setTimeout(() => setDeleting(true), pause);
    } else if (deleting && text === "") {
      setDeleting(false);
      setIndex((i) => i + 1);
    } else {
      timer = setTimeout(
        () =>
          setText(
            deleting ? word.slice(0, text.length - 1) : word.slice(0, text.length + 1)
          ),
        deleting ? deleteSpeed : typeSpeed
      );
    }
    return () => clearTimeout(timer);
  }, [text, deleting, index, words, typeSpeed, deleteSpeed, pause]);

  return text;
}

function useInView(threshold = 0.2) {
  const ref = useRef(null);
  const [inView, setInView] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el || typeof IntersectionObserver === "undefined") {
      setInView(true);
      return;
    }
    const obs = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setInView(true);
          obs.disconnect();
        }
      },
      { threshold }
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, [threshold]);
  return [ref, inView];
}

function Reveal({ children, delay = 0, className = "" }) {
  const [ref, inView] = useInView(0.15);
  return (
    <div
      ref={ref}
      className={`reveal ${inView ? "reveal-in" : ""} ${className}`}
      style={{ transitionDelay: `${delay}ms` }}
    >
      {children}
    </div>
  );
}

/* ------------------------------------------------------------------
   3. Shared pieces
------------------------------------------------------------------ */

// Swap this for <img src="..." /> once you have real screenshots.
function Placeholder({ label, hue = 210, className = "", big = false }) {
  return (
    <div
      className={`relative flex items-center justify-center overflow-hidden ${className}`}
      style={{
        background: `linear-gradient(135deg, hsl(${hue} 60% 22%), hsl(${hue + 35} 70% 12%))`,
      }}
    >
      <div className="pointer-events-none absolute inset-0 opacity-30 grid-overlay" />
      <span
        className={`relative px-4 text-center font-semibold tracking-wide text-white/70 ${
          big ? "text-base" : "text-xs"
        }`}
      >
        {label}
      </span>
    </div>
  );
}

// Shows the real photo, and falls back to the gradient block if it can't load.
function Photo({ src, alt, className = "", imgClassName = "", fallback, hue = 215 }) {
  const [failed, setFailed] = useState(false);
  if (failed || !src) {
    return <Placeholder label={fallback} hue={hue} big className={className} />;
  }
  return (
    <div className={`overflow-hidden ${className}`}>
      <img
        src={src}
        alt={alt}
        onError={() => setFailed(true)}
        className={`h-full w-full object-cover ${imgClassName}`}
      />
    </div>
  );
}

function SkillRing({ name, level, active }) {
  const R = 46;
  const C = 2 * Math.PI * R;
  return (
    <div className="flex flex-col items-center">
      <div className="relative h-32 w-32">
        <svg viewBox="0 0 100 100" className="h-full w-full -rotate-90">
          <circle cx="50" cy="50" r={R} fill="none" stroke="#334155" strokeWidth="10" />
          <circle
            cx="50"
            cy="50"
            r={R}
            fill="none"
            stroke="#3b82f6"
            strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={C}
            strokeDashoffset={active ? C - (C * level) / 100 : C}
            style={{ transition: "stroke-dashoffset 1.2s cubic-bezier(.22,.8,.3,1)" }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-base font-semibold text-slate-100">{name}</span>
          <span className="text-base font-bold text-blue-400">{level}%</span>
        </div>
      </div>
    </div>
  );
}

function SectionTitle({ children, sub }) {
  return (
    <div className="mb-12 text-center">
      <h2 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
        {children}
      </h2>
      <div className="mx-auto mt-4 h-1 w-16 rounded-full bg-blue-500" />
      {sub && <p className="mt-4 text-slate-400">{sub}</p>}
    </div>
  );
}

/* ------------------------------------------------------------------
   4. Navbar
------------------------------------------------------------------ */

function Navbar({ active, onNavigate, onHome, compact }) {
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const go = (id) => {
    setOpen(false);
    onNavigate(id);
  };

  return (
    <header
      className={`fixed inset-x-0 top-0 z-50 transition-all duration-300 ${
        scrolled
          ? "bg-slate-950/90 shadow-lg shadow-black/40 backdrop-blur"
          : "bg-slate-950/60 backdrop-blur-sm"
      }`}
    >
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4">
        <button
          onClick={onHome}
          className="flex items-center gap-3 rounded focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-400"
        >
          <img
            src={PROFILE.photo}
            alt={PROFILE.name}
            className="h-10 w-10 rounded-md object-cover ring-1 ring-white/10"
          />
          <span className="text-lg font-bold text-white">Portfolio {PROFILE.handle}</span>
        </button>

        <ul className="hidden items-center gap-8 md:flex">
          {NAV.map((item) => (
            <li key={item.id}>
              <button
                onClick={() => go(item.id)}
                className={`text-sm font-medium transition-colors hover:text-blue-400 ${
                  active === item.id && !compact ? "text-blue-500" : "text-slate-300"
                }`}
              >
                {item.label}
              </button>
            </li>
          ))}
        </ul>

        <button
          className="rounded p-2 text-slate-200 md:hidden"
          onClick={() => setOpen((o) => !o)}
          aria-label={open ? "Close menu" : "Open menu"}
          aria-expanded={open}
        >
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </nav>

      {open && (
        <ul className="border-t border-white/5 bg-slate-950 px-5 pb-4 md:hidden">
          {NAV.map((item) => (
            <li key={item.id}>
              <button
                onClick={() => go(item.id)}
                className="block w-full py-3 text-left text-slate-200"
              >
                {item.label}
              </button>
            </li>
          ))}
        </ul>
      )}
    </header>
  );
}

/* ------------------------------------------------------------------
   5. Sections
------------------------------------------------------------------ */

function Hero({ onNavigate }) {
  const typed = useTypewriter(PROFILE.roles);
  return (
    <section id="home" className="relative flex min-h-screen items-center overflow-hidden pt-20">
      <div className="absolute inset-0 bg-slate-950" />
      <div className="absolute inset-0 grid-overlay opacity-40" />
      <div className="absolute -left-24 top-1/3 h-72 w-72 rounded-full bg-blue-600/20 blur-3xl" />

      <div className="relative mx-auto grid w-full max-w-7xl items-center gap-10 px-5 md:grid-cols-2">
        <div className="order-2 md:order-1">
          <div className="relative mx-auto w-full max-w-sm">
            <div className="absolute -inset-6 rounded-full bg-blue-600/20 blur-3xl" />
            <Photo
              src={PROFILE.photo}
              alt={PROFILE.name}
              fallback="Add profile.jpg to /public"
              hue={215}
              className="relative aspect-square w-full rounded-2xl ring-1 ring-white/10 photo-fade"
              imgClassName="object-top"
            />
          </div>
        </div>

        <div className="order-1 text-center md:order-2 md:text-left">
          <h1 className="text-4xl font-extrabold leading-tight tracking-tight text-white sm:text-5xl lg:text-6xl">
            Hello, I'm {PROFILE.name}
          </h1>
          <p className="mt-6 text-2xl font-bold text-blue-500 sm:text-3xl">
            {typed}
            <span className="caret">|</span>
          </p>
          <div className="mt-10 flex flex-col items-center gap-4 sm:flex-row md:justify-start">
            <button
              onClick={() => onNavigate("projects")}
              className="rounded-md bg-blue-600 px-7 py-3 font-semibold text-white shadow-lg shadow-blue-900/40 transition hover:bg-blue-500"
            >
              View my work
            </button>
            <a
              href={PROFILE.cvUrl}
              download
              className="flex items-center gap-2 rounded-md bg-blue-600 px-7 py-3 font-semibold text-white shadow-lg shadow-blue-900/40 transition hover:bg-blue-500"
            >
              <Download size={18} /> Download CV
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}

function About() {
  const [ref, inView] = useInView(0.2);
  return (
    <section id="about" className="bg-slate-900 py-24">
      <div className="mx-auto max-w-7xl px-5">
        <SectionTitle>About me</SectionTitle>
        <div className="mx-auto max-w-4xl">
          <div className="rounded-2xl bg-slate-950/60 ring-1 ring-white/5 p-8 md:p-10">
            <div className="flex flex-col items-center gap-8 md:flex-row md:items-start">
              <Reveal>
                <div className="shrink-0">
                  <Photo
                    src={PROFILE.photo}
                    alt={PROFILE.name}
                    fallback="Add profile.jpg to /public"
                    hue={220}
                    className="mx-auto h-48 w-48 rounded-full ring-8 ring-slate-800"
                    imgClassName="object-top"
                  />
                </div>
              </Reveal>

              <Reveal delay={120}>
                <div>
                  <p className="text-slate-300">{PROFILE.intro}</p>

                  <h3 className="mt-6 text-lg font-semibold text-white">Education</h3>
                  <ul className="mt-3 space-y-2">
                    {EDUCATION.map((e) => (
                      <li key={e.label} className="flex gap-2 text-slate-300">
                        <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-blue-500" />
                        <span>
                          <strong className="font-semibold text-white">{e.label}:</strong> {e.value}
                        </span>
                      </li>
                    ))}
                  </ul>

                  <h3 className="mt-6 text-lg font-semibold text-white">Experience</h3>
                  <ul className="mt-3 space-y-3">
                    {EXPERIENCE.map((e) => (
                      <li key={e.role + e.org} className="rounded-lg border border-white/5 bg-slate-900/40 p-3">
                        <p className="font-semibold text-white">{e.role}</p>
                        <p className="text-sm text-slate-400">{e.org} · {e.period}</p>
                      </li>
                    ))}
                  </ul>

                  <h3 className="mt-6 text-2xl font-bold tracking-tight text-white">Skills</h3>
                  <div ref={ref} className="mt-4 grid grid-cols-4 gap-4 sm:grid-cols-4 justify-center">
                    {SKILLS.map((s) => (
                      <div key={s.name} className="flex items-center justify-center">
                        <SkillRing {...s} active={inView} />
                      </div>
                    ))}
                  </div>

                  <div className="mt-6 space-y-3">
                    {TOOLBOX.map((t) => (
                      <div key={t.group} className="sm:flex sm:gap-4">
                        <p className="w-32 shrink-0 text-sm font-semibold text-slate-400">{t.group}</p>
                        <ul className="mt-2 flex flex-wrap gap-2 sm:mt-0">
                          {t.items.map((i) => (
                            <li key={i} className="rounded-md border border-white/10 bg-slate-900/40 px-2.5 py-1 text-xs text-slate-300">
                              {i}
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}

                    <div className="sm:flex sm:gap-4">
                      <p className="w-32 shrink-0 text-sm font-semibold text-slate-400">Languages</p>
                      <p className="mt-2 text-sm text-slate-300 sm:mt-0">{LANGUAGES.join(" · ")}</p>
                    </div>

                    <div className="sm:flex sm:gap-4">
                      <p className="w-32 shrink-0 text-sm font-semibold text-slate-400">Activities</p>
                      <p className="mt-2 text-sm text-slate-300 sm:mt-0">Member, Photography Society — Dharmasoka College (2016–2020)</p>
                    </div>
                  </div>
                </div>
              </Reveal>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function Services() {
  return (
    <section id="services" className="bg-slate-950 py-24">
      <div className="mx-auto max-w-7xl px-5">
        <SectionTitle>Services</SectionTitle>
        <div className="grid gap-6 md:grid-cols-3">
          {SERVICES.map((s, i) => (
            <Reveal key={s.title} delay={i * 100}>
              <article className="h-full rounded-xl border border-white/5 bg-slate-900/70 p-8 text-center transition duration-300 hover:-translate-y-1 hover:border-blue-500/40 hover:shadow-xl hover:shadow-blue-950/50">
                <s.icon className="mx-auto text-blue-500" size={44} strokeWidth={1.8} />
                <h3 className="mt-5 text-xl font-bold text-white">{s.title}</h3>
                <p className="mt-3 text-slate-400">{s.body}</p>
              </article>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}

function Projects({ onOpen }) {
  return (
    <section id="projects" className="bg-slate-900 py-24">
      <div className="mx-auto max-w-7xl px-5">
        <SectionTitle sub="Explore my recent projects and creative work">My portfolio</SectionTitle>
        <div className="mx-auto grid max-w-5xl gap-8 sm:grid-cols-2">
          {PROJECTS.map((p, i) => (
            <Reveal key={p.id} delay={i * 100}>
              <article className="group flex h-full flex-col overflow-hidden rounded-xl border border-white/5 bg-slate-950/60 transition duration-300 hover:-translate-y-1 hover:border-blue-500/40 hover:shadow-xl hover:shadow-blue-950/50">
                <Placeholder
                  label={`${p.cardTitle} — cover`}
                  hue={p.hue}
                  className="aspect-video w-full"
                />
                <div className="flex flex-1 flex-col p-6">
                  <p className="text-xs font-semibold uppercase tracking-widest text-blue-400">
                    {p.kind}
                  </p>
                  <h3 className="mt-2 text-lg font-bold text-white">{p.cardTitle}</h3>
                  <p className="mt-2 text-sm text-slate-400">{p.tagline}</p>
                  <ul className="mt-4 flex flex-wrap gap-2">
                    {p.tech.slice(0, 4).map((t) => (
                      <li
                        key={t}
                        className="rounded-full border border-blue-500/40 px-3 py-1 text-xs text-blue-300"
                      >
                        {t}
                      </li>
                    ))}
                  </ul>
                  <button
                    onClick={() => onOpen(p.id)}
                    className="mt-6 self-start text-sm font-semibold text-blue-400 transition group-hover:text-blue-300"
                  >
                    View project →
                  </button>
                </div>
              </article>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}

function Contact() {
  const [form, setForm] = useState({ name: "", subject: "", email: "", message: "" });
  const [state, setState] = useState({ status: "idle", note: "" });

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const mailtoHref = `mailto:${PROFILE.email}?subject=${encodeURIComponent(
    form.subject || `Portfolio enquiry from ${form.name || "your site"}`
  )}&body=${encodeURIComponent(`${form.message}\n\n— ${form.name} (${form.email})`)}`;

  const send = async () => {
    const valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email);
    if (!form.name.trim() || !form.message.trim()) {
      setState({ status: "error", note: "Add your name and a message before sending." });
      return;
    }
    if (!valid) {
      setState({ status: "error", note: "That email address doesn't look right." });
      return;
    }

    setState({ status: "sending", note: "" });
    try {
      const res = await fetch(FORM_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({
          name: form.name,
          email: form.email,
          _subject: form.subject || `Portfolio enquiry from ${form.name}`,
          message: form.message,
          _template: "table",
          _captcha: "false",
        }),
      });
      if (!res.ok) throw new Error("Request failed");
      setState({
        status: "sent",
        note: `Message sent. I'll reply to ${form.email}.`,
      });
      setForm({ name: "", subject: "", email: "", message: "" });
    } catch {
      setState({
        status: "error",
        note: "Couldn't send from here. Use the mail app link below instead.",
      });
    }
  };

  const field =
    "w-full rounded-lg border border-white/10 bg-slate-900/70 px-4 py-3 text-slate-100 placeholder-slate-500 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30";

  return (
    <section id="contact" className="bg-slate-950 py-24">
      <div className="mx-auto max-w-7xl px-5">
        <SectionTitle>Contact me</SectionTitle>
        <div className="grid gap-10 md:grid-cols-2">
          <Reveal>
            <div className="space-y-5 rounded-2xl border border-white/5 bg-slate-900/50 p-8">
              {[
                { k: "name", label: "Name", ph: "Your name" },
                { k: "subject", label: "Subject", ph: "Subject" },
                { k: "email", label: "Email", ph: "Your email", type: "email" },
              ].map((f) => (
                <div key={f.k}>
                  <label
                    htmlFor={f.k}
                    className="mb-2 block text-center text-xs font-bold uppercase tracking-widest text-slate-300"
                  >
                    {f.label}
                  </label>
                  <input
                    id={f.k}
                    type={f.type || "text"}
                    value={form[f.k]}
                    onChange={set(f.k)}
                    placeholder={f.ph}
                    className={field}
                  />
                </div>
              ))}
              <div>
                <label
                  htmlFor="message"
                  className="mb-2 block text-center text-xs font-bold uppercase tracking-widest text-slate-300"
                >
                  Message
                </label>
                <textarea
                  id="message"
                  rows={5}
                  value={form.message}
                  onChange={set("message")}
                  placeholder="Your message"
                  className={field}
                />
              </div>
              <button
                onClick={send}
                disabled={state.status === "sending"}
                className="flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
              >
                <Send size={18} />
                {state.status === "sending" ? "Sending…" : "Send message"}
              </button>

              {state.note && (
                <p
                  role="status"
                  className={`text-center text-sm ${
                    state.status === "error" ? "text-amber-300" : "text-blue-300"
                  }`}
                >
                  {state.note}
                </p>
              )}

              <a
                href={mailtoHref}
                className="block text-center text-sm text-slate-400 underline-offset-4 hover:text-blue-400 hover:underline"
              >
                Or open this in your mail app
              </a>
            </div>
          </Reveal>

          <Reveal delay={120}>
            <ul className="space-y-5">
              <li className="flex items-center gap-4 text-slate-200">
                <Mail className="text-blue-500" size={22} />
                <a href={`mailto:${PROFILE.email}`} className="hover:text-blue-400">
                  {PROFILE.email}
                </a>
              </li>
              <li className="flex items-center gap-4 text-slate-200">
                <Phone className="text-blue-500" size={22} />
                <a href={`tel:${PROFILE.phone}`} className="hover:text-blue-400">
                  {PROFILE.phone}
                </a>
              </li>
              <li className="flex items-center gap-4 text-slate-200">
                <MapPin className="text-blue-500" size={22} />
                {PROFILE.address}
              </li>
            </ul>

            <div className="mt-8 overflow-hidden rounded-2xl border border-white/5 bg-slate-900/50 p-3">
              <iframe
                title="Location map"
                className="h-64 w-full rounded-xl"
                loading="lazy"
                referrerPolicy="no-referrer-when-downgrade"
                src={`https://www.google.com/maps?q=${encodeURIComponent(
                  PROFILE.mapQuery
                )}&output=embed`}
              />
            </div>
          </Reveal>
        </div>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer className="border-t border-white/5 bg-slate-950 py-8">
      <div className="mx-auto flex max-w-7xl flex-col items-center gap-4 px-5">
        <div className="flex gap-5">
          <a
            href={PROFILE.github}
            target="_blank"
            rel="noreferrer"
            aria-label="GitHub"
            className="text-slate-400 transition hover:text-blue-400"
          >
            <GithubIcon size={20} />
          </a>
          <a
            href={PROFILE.linkedin}
            target="_blank"
            rel="noreferrer"
            aria-label="LinkedIn"
            className="text-slate-400 transition hover:text-blue-400"
          >
            <LinkedinIcon size={20} />
          </a>
          <a
            href={`mailto:${PROFILE.email}`}
            aria-label="Email"
            className="text-slate-400 transition hover:text-blue-400"
          >
            <Mail size={20} />
          </a>
        </div>
        <p className="text-sm text-slate-400">
          © {new Date().getFullYear()} {PROFILE.name}. All rights reserved.
        </p>
      </div>
    </footer>
  );
}

/* ------------------------------------------------------------------
   6. Project detail page
------------------------------------------------------------------ */

function ProjectPage({ project, onBack }) {
  const [i, setI] = useState(0);
  const count = project.shots.length;

  const next = useCallback(() => setI((v) => (v + 1) % count), [count]);
  const prev = () => setI((v) => (v - 1 + count) % count);

  useEffect(() => {
    const t = setInterval(next, 5000);
    return () => clearInterval(t);
  }, [next]);

  return (
    <main className="bg-slate-950 pt-24">
      <div className="mx-auto max-w-6xl px-5 pb-24">
        <button
          onClick={onBack}
          className="mb-8 flex items-center gap-2 text-sm font-semibold text-slate-400 transition hover:text-blue-400"
        >
          <ArrowLeft size={16} /> Back to portfolio
        </button>

        <p className="text-center text-xs font-semibold uppercase tracking-widest text-blue-400">
          {project.kind}
        </p>
        <h1 className="mt-3 text-center text-3xl font-extrabold tracking-tight text-white sm:text-5xl">
          {project.title}
        </h1>

        {/* Carousel */}
        <div className="relative mt-12 overflow-hidden rounded-2xl border border-white/10 bg-slate-900">
          <Placeholder
            label={`${project.shots[i]} — screenshot ${i + 1} of ${count}`}
            hue={project.hue + i * 12}
            big
            className="aspect-video w-full"
          />
          <button
            onClick={prev}
            aria-label="Previous screenshot"
            className="absolute left-4 top-1/2 grid h-11 w-11 -translate-y-1/2 place-items-center rounded-full bg-black/50 text-white backdrop-blur transition hover:bg-black/70"
          >
            <ChevronLeft size={22} />
          </button>
          <button
            onClick={next}
            aria-label="Next screenshot"
            className="absolute right-4 top-1/2 grid h-11 w-11 -translate-y-1/2 place-items-center rounded-full bg-black/50 text-white backdrop-blur transition hover:bg-black/70"
          >
            <ChevronRight size={22} />
          </button>
          <div className="flex items-center justify-center gap-2 bg-slate-900 py-4">
            {project.shots.map((s, idx) => (
              <button
                key={s}
                onClick={() => setI(idx)}
                aria-label={`Show ${s}`}
                className={`h-2.5 rounded-full transition-all ${
                  idx === i ? "w-7 bg-blue-500" : "w-2.5 bg-slate-600 hover:bg-slate-500"
                }`}
              />
            ))}
          </div>
        </div>

        {/* White content card, like the reference */}
        <div className="mt-12 rounded-3xl bg-white p-8 text-slate-800 shadow-2xl sm:p-12">
          <h2 className="text-3xl font-extrabold text-slate-900">About this project</h2>
          <div className="mt-4 h-0.5 w-full bg-blue-500/70" />
          {project.about.map((p) => (
            <p key={p} className="mt-6 leading-relaxed text-slate-600">
              {p}
            </p>
          ))}

          <h2 className="mt-14 text-3xl font-extrabold text-slate-900">Technologies used</h2>
          <div className="mt-4 h-0.5 w-full bg-blue-500/70" />
          <ul className="mt-6 flex flex-wrap gap-3">
            {project.tech.map((t) => (
              <li
                key={t}
                className="rounded-full border border-blue-300 bg-blue-50 px-4 py-1.5 text-sm text-blue-600"
              >
                {t}
              </li>
            ))}
          </ul>

          <h2 className="mt-14 text-3xl font-extrabold text-slate-900">Key features</h2>
          <div className="mt-4 h-0.5 w-full bg-blue-500/70" />
          <ul className="mt-6 space-y-4">
            {project.features.map((f) => (
              <li key={f} className="flex items-start gap-3 text-slate-700">
                <CheckCircle2 className="mt-0.5 shrink-0 text-blue-500" size={22} />
                {f}
              </li>
            ))}
          </ul>

          <div className="mt-12 flex flex-col justify-center gap-4 sm:flex-row">
            {project.live && (
              <a
                href={project.live}
                target="_blank"
                rel="noreferrer"
                className="flex items-center justify-center gap-2 rounded-full bg-blue-500 px-8 py-4 font-semibold text-white shadow-lg transition hover:bg-blue-600"
              >
                <Globe size={20} /> View live site
              </a>
            )}
            <a
              href={project.repo}
              target="_blank"
              rel="noreferrer"
              className="flex items-center justify-center gap-2 rounded-full bg-slate-800 px-8 py-4 font-semibold text-white shadow-lg transition hover:bg-slate-700"
            >
              <GithubIcon size={20} /> View on GitHub
            </a>
          </div>
        </div>
      </div>
      <Footer />
    </main>
  );
}

/* ------------------------------------------------------------------
   7. App
------------------------------------------------------------------ */

export default function Portfolio() {
  const [route, setRoute] = useState(null); // null = home, otherwise project id
  const [active, setActive] = useState("home");

  const project = useMemo(() => PROJECTS.find((p) => p.id === route), [route]);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "auto" });
  }, [route]);

  useEffect(() => {
    if (route) return;
    const onScroll = () => {
      const y = window.scrollY + 140;
      let current = "home";
      NAV.forEach((n) => {
        const el = document.getElementById(n.id);
        if (el && el.offsetTop <= y) current = n.id;
      });
      setActive(current);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, [route]);

  const navigate = (id) => {
    if (route) {
      setRoute(null);
      setTimeout(() => document.getElementById(id)?.scrollIntoView({ behavior: "smooth" }), 60);
    } else {
      document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 font-sans antialiased selection:bg-blue-600 selection:text-white">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
        .font-sans { font-family: 'Outfit', ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif; }
        .grid-overlay {
          background-image:
            linear-gradient(rgba(148,163,184,.06) 1px, transparent 1px),
            linear-gradient(90deg, rgba(148,163,184,.06) 1px, transparent 1px);
          background-size: 44px 44px;
        }
        .photo-fade img {
          -webkit-mask-image: radial-gradient(circle at 50% 42%, #000 58%, transparent 78%);
          mask-image: radial-gradient(circle at 50% 42%, #000 58%, transparent 78%);
        }
        .caret { animation: blink 1s steps(1) infinite; }
        @keyframes blink { 50% { opacity: 0; } }
        .reveal { opacity: 0; transform: translateY(24px); transition: opacity .7s ease, transform .7s cubic-bezier(.22,.8,.3,1); }
        .reveal-in { opacity: 1; transform: none; }
        html { scroll-behavior: smooth; }
        @media (prefers-reduced-motion: reduce) {
          html { scroll-behavior: auto; }
          .reveal { opacity: 1; transform: none; transition: none; }
          .caret { animation: none; }
        }
      `}</style>

      <Navbar
        active={active}
        compact={Boolean(route)}
        onNavigate={navigate}
        onHome={() => (route ? setRoute(null) : navigate("home"))}
      />

      {project ? (
        <ProjectPage project={project} onBack={() => setRoute(null)} />
      ) : (
        <main>
          <Hero onNavigate={navigate} />
          <About />
          <Services />
          <Projects onOpen={setRoute} />
          <Contact />
          <Footer />
        </main>
      )}
    </div>
  );
}
