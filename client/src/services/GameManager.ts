import APIDataConsumer from './core/APIDataConsumer';
import { Game } from '../types/game.interface';

export class GameManager {
  public static async requestGameData(
    name: string,
    secs: string
  ): Promise<Game> {
    const normalizedPayload = GameManager.normalizePayload(name, secs);
    const { data: response } = await APIDataConsumer.makePostRequest(
      normalizedPayload
    );
    return Game.fromJSON(response);
  }

  public static normalizePayload(name: string, secs: string) {
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
