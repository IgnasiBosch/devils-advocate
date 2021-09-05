var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
import 'reflect-metadata';
import { Expose, plainToClass, Type } from 'class-transformer';
export class Game {
    id;
    status;
    secsPerRound;
    joinLink;
    player;
    static fromJSON(plainGame) {
        return plainToClass(Game, plainGame, { excludeExtraneousValues: true });
    }
}
__decorate([
    Expose()
], Game.prototype, "id", void 0);
__decorate([
    Expose()
], Game.prototype, "status", void 0);
__decorate([
    Expose()
], Game.prototype, "secsPerRound", void 0);
__decorate([
    Expose()
], Game.prototype, "joinLink", void 0);
__decorate([
    Type(() => Player),
    Expose()
], Game.prototype, "player", void 0);
class Player {
    id;
    name;
    score;
}
__decorate([
    Expose()
], Player.prototype, "id", void 0);
__decorate([
    Expose()
], Player.prototype, "name", void 0);
__decorate([
    Expose()
], Player.prototype, "score", void 0);
//# sourceMappingURL=game.interface.js.map