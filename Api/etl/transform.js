
export function calculerIndicateurs(sensorData, nbApnees, nbHypopnees, nbRera, nbEvents) {
    // Conversion sécurisée en nombre pour éviter les erreurs NaN
    const spo2Values = sensorData.map(d => parseFloat(d.spo2) || 0);
    const dbValues = sensorData.map(d => parseFloat(d.ronflements_db) || 0);
    const positions = sensorData.map(d => d.position);

    //calculate median
    const getMedian = (arr) => {
        const sorted = [...arr].sort((a, b) => a - b);
        const mid = Math.floor(sorted.length / 2);
        return sorted.length % 2 !== 0 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
    };

    // calculate mode
    const getMode = (arr) => {
        const counts = arr.reduce((acc, val) => { acc[val] = (acc[val] || 0) + 1; return acc; }, {});
        return Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b, "Inconnue");
    };

    const stats = {
        spo2_min: Math.min(...spo2Values),
        spo2_moy: spo2Values.reduce((a, b) => a + b, 0) / spo2Values.length,
        spo2_mediane: getMedian(spo2Values),
        decibels_max: Math.max(...dbValues),
        decibels_moy: dbValues.reduce((a, b) => a + b, 0) / dbValues.length,
        nbronflementsforts: dbValues.filter(db => db > 70).length,
        position_dominante: getMode(positions),
        dureehypoxiemin: spo2Values.filter(s => s < 90).length * (10 / 60),

        nb_apnees: nbApnees?.[0] ?? 0,
        nb_hypopnees: nbHypopnees?.[0] ?? 0,
        nb_rera: nbRera?.[0] ?? 0,
        nb_microeveils: nbEvents?.[0] ?? 0
    };

    return stats;
}