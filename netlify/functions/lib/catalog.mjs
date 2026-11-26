import data from '../../../data/programs.json' with { type: 'json' };
export const findProgram = (id) => data.programs.find((p) => p.id === id && typeof p.price === 'number' && p.price > 0);
