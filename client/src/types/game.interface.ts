import 'reflect-metadata';
import { Expose, plainToClass, Type } from 'class-transformer';

export class Game {
  @Expose() public id: number;
  @Expose() public status: string;
  @Expose() public secsPerRound: number;
  @Expose() public joinLink: string;
  @Type(() => Player)
  @Expose()
  public player: Player[];

  static fromJSON(plainGame: object) {
    return plainToClass(Game, plainGame, { excludeExtraneousValues: true });
  }
}

class Player {
  @Expose() public id: number;
  @Expose() public name: string;
  @Expose() public score: number;
}
