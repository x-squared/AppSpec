import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from 'react';
import translationsAppSpecConfig from './translations.appspec.json';
import translationsBaseConfig from './translations.base.json';

export type AppLocale = 'en' | 'de';
export type TranslationMap = Record<string, string>;

interface TranslationLeafNode {
  label?: Record<string, string>;
  text?: Record<string, string>;
}

type TranslationNode = TranslationLeafNode | Record<string, unknown>;

interface BuiltinTranslationConfig {
  translationsByLocale: Record<string, TranslationMap>;
  labelsByKey: Record<string, Record<string, string>>;
}

const isRecord = (value: unknown): value is Record<string, unknown> => (
  typeof value === 'object' && value !== null && !Array.isArray(value)
);

const isLeafNode = (value: unknown): value is TranslationLeafNode => (
  isRecord(value) && (isRecord(value.text) || isRecord(value.label))
);

function mergeTranslationBundles(...bundles: Record<string, unknown>[]): Record<string, unknown> {
  const merge = (target: Record<string, unknown>, source: Record<string, unknown>): Record<string, unknown> => {
    const next: Record<string, unknown> = { ...target };
    Object.entries(source).forEach(([key, value]) => {
      const existing = next[key];
      if (isRecord(existing) && isRecord(value)) {
        next[key] = merge(existing, value);
        return;
      }
      next[key] = value;
    });
    return next;
  };
  return bundles.reduce<Record<string, unknown>>((acc, bundle) => merge(acc, bundle), {});
}

function buildBuiltinTranslationConfig(root: Record<string, unknown>): BuiltinTranslationConfig {
  const translationsByLocale: Record<string, TranslationMap> = {};
  const labelsByKey: Record<string, Record<string, string>> = {};

  const walk = (node: TranslationNode, path: string[]) => {
    if (isLeafNode(node)) {
      const key = path.join('.');
      if (isRecord(node.text)) {
        Object.entries(node.text).forEach(([localeKey, textValue]) => {
          if (typeof textValue !== 'string') return;
          if (!translationsByLocale[localeKey]) translationsByLocale[localeKey] = {};
          translationsByLocale[localeKey][key] = textValue;
        });
      }
      if (isRecord(node.label)) {
        labelsByKey[key] = {};
        Object.entries(node.label).forEach(([localeKey, labelValue]) => {
          if (typeof labelValue === 'string') labelsByKey[key][localeKey] = labelValue;
        });
      }
      return;
    }
    if (!isRecord(node)) return;
    Object.entries(node).forEach(([nextKey, nextNode]) => {
      if (!isRecord(nextNode)) return;
      walk(nextNode as TranslationNode, [...path, nextKey]);
    });
  };

  walk(root, []);
  return { translationsByLocale, labelsByKey };
}

const builtinTranslationsRoot = mergeTranslationBundles(
  translationsBaseConfig as Record<string, unknown>,
  translationsAppSpecConfig as Record<string, unknown>,
);
const builtinTranslationConfig = buildBuiltinTranslationConfig(builtinTranslationsRoot);
const builtinTranslationsByLocale = builtinTranslationConfig.translationsByLocale;
export const translationItemLabelsByKey = builtinTranslationConfig.labelsByKey;
export function getBuiltinTranslationsForLocale(locale: string): TranslationMap {
  return builtinTranslationsByLocale[locale] ?? {};
}

interface I18nContextValue {
  locale: AppLocale;
  setLocale: (nextLocale: AppLocale) => void;
  t: (key: string, englishDefault: string) => string;
  runtimeTranslations: TranslationMap;
  setRuntimeTranslations: (nextTranslations: TranslationMap) => void;
}

const I18nContext = createContext<I18nContextValue | null>(null);

export function I18nProvider({ children }: { children: ReactNode }) {
  const [locale, setLocaleState] = useState<AppLocale>('en');
  const [runtimeTranslations, setRuntimeTranslationsState] = useState<TranslationMap>({});

  const setLocale = useCallback((nextLocale: AppLocale) => {
    setLocaleState(nextLocale);
  }, []);

  const setRuntimeTranslations = useCallback((nextTranslations: TranslationMap) => {
    setRuntimeTranslationsState({ ...nextTranslations });
  }, []);

  const t = useCallback((key: string, englishDefault: string): string => {
    const builtinByLocale = builtinTranslationsByLocale[locale] ?? {};
    return runtimeTranslations[key] ?? builtinByLocale[key] ?? englishDefault;
  }, [runtimeTranslations, locale]);

  const value = useMemo<I18nContextValue>(() => ({
    locale,
    setLocale,
    t,
    runtimeTranslations,
    setRuntimeTranslations,
  }), [runtimeTranslations, locale, setRuntimeTranslations, setLocale, t]);

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useI18n(): I18nContextValue {
  const ctx = useContext(I18nContext);
  if (!ctx) throw new Error('useI18n must be used within I18nProvider');
  return ctx;
}

