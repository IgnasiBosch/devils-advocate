import APIDataConsumer from './core/APIDataConsumer';
import { Game } from '../types/game.interface';
export class GameManager {
    static async requestGameData(name, secs) {
        const normalizedPayload = GameManager.normalizePayload(name, secs);
        const { data: response } = await APIDataConsumer.makePostRequest(normalizedPayload);
        return Game.fromJSON(response);
    }
    static normalizePayload(name, secs) {
        return {
            player: {
                name,
            },
            game: {
                secsPerRound: +secs,
            },
        };
    }
}
//# sourceMappingURL=GameManager.js.map