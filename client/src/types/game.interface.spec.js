import { Game } from './game.interface';
describe('Game', () => {
    it('should convert a plain JSON into a Game object', () => {
        // Arrange.
        const payload = {
            id: 0,
            status: 'foo',
            secsPerRound: 1,
            joinLink: 'link',
            player: [
                {
                    id: 0,
                    score: 0,
                    kjldsf: 0,
                },
            ],
        };
        // Act.
        const sut = Game.fromJSON(payload);
        // Assert.
    });
});
//# sourceMappingURL=game.interface.spec.js.map